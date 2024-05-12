import os
import yaml
import pandas as pd
import re
import glob
from transformers import GPT2TokenizerFast


def build_example_prompt(input_label, input_value, output_label=None, output_value=None, base_prompt=None, is_example=True):
    input_value =  re.sub("\s+", " ", input_value)
    input_prompt = f"{base_prompt or ''}{'Example:' if is_example else ''}\n{input_label}:\n{input_value}"
    example_prompt = [
        {
            "role": "user",
            "content": input_prompt
        }
    ]

    if output_label:
        output_prompt = f"{output_label}:\n{output_value or ''}"
        if is_example:
            output_prompt += "\n\n"
        example_prompt.append({
            "role": "assistant",
            "content": output_prompt
        })

    return example_prompt


def build_examples_prompt(
    strategy: str, 
    examples_df: pd.DataFrame, 
    input_data: object = None, 
    headless: bool=False, 
    limit: int=10,
    seed: int=42,
    config_path: str = './config/prompts'
):    
    strategies = load_strategies(filepath=os.path.join(config_path, "prompt_strategies.yml"))
    if strategy not in strategies:
        raise ValueError(f"Strategy {strategy} not found in {strategies.keys()}")
    
    properties = strategies[strategy]
    
    example_prompts = []
    if (examples_df is not None) and (not examples_df.empty):
        data = examples_df.sample(n=limit, random_state=seed) if len(examples_df) > limit else examples_df
        for index, (_, row) in enumerate(data.iterrows()):
            example_prompt = build_example_prompt(
                input_value=row[properties["input_column"]], 
                input_label=properties["input_label"],
                output_value=row[properties["output_column"]],
                output_label=properties["output_label"],
                base_prompt=properties["user_prompt_examples"] if index == 0 else "",
            )
            example_prompts += example_prompt

    if headless:
        prompt = example_prompts
    else:
        prompt = [{
            "role": "system", 
            "content": properties["system_prompt"]
        }] 
        
        prompt += example_prompts
        
        if input_data is not None:
            input_prompt = build_example_prompt(
                input_label=properties["input_label"],
                input_value=input_data[properties["input_column"]], 
                # output_label=properties["output_label"],
                # output_value=input_data[properties["output_column"]] if properties["output_column"] in input_data else None,
                is_example=False
            )
            previous_examples_context = "Based on the previous examples, " if example_prompts else ""
            prediction_instruction = previous_examples_context + properties["prediction_prompt"]
            input_prompt[0]["content"] = prediction_instruction + input_prompt[0]["content"]
            
            prompt += input_prompt
    
    return prompt


def build_spec_prompt(
    strategy: str, 
    files_path: str = 'content/**/*.txt', 
    config_path: str = './config/prompts',
    input_data: object = None, 
    examples_df: pd.DataFrame = None, 
    examples_limit: int = 0,
    headless: bool=False,
    seed: int=42,
):
    strategies = load_strategies(filepath=os.path.join(config_path, "prompt_strategies.yml"))
    if strategy not in strategies:
        raise ValueError(f"Strategy {strategy} not found in {strategies.keys()}")
    
    properties = strategies[strategy]
    
    prompt_dict = {}
    path = os.path.join(config_path, files_path)
    for prompt_file in glob.glob(path):
        key = os.path.basename(prompt_file).split('.')[0].lower()
        with open(prompt_file, "r") as f:
            prompt_dict[key] = f.read()
    
    spec = ""
    for key, value in prompt_dict.items():
        spec += f"# {key.upper()}:\n\n{value}\n\n"
    prompt = properties["user_prompt_spec"] + "\nAPI Specifications:\n" + spec

    spec_prompt = [{
        "role": "user",
        "content": prompt
    },
    {
        "role": "assistant",
        "content": "ok"
    }]
    
    if examples_limit > 0 and examples_df is not None:
        spec_prompt += build_examples_prompt(strategy=strategy, examples_df=examples_df, limit=examples_limit, headless=True, seed=seed, config_path=config_path)
            
    if headless:
        prompt = spec_prompt
    else:
        prompt = [{
            "role": "system", 
            "content": properties["system_prompt"]
        }] 
        
        prompt += spec_prompt
        
        if input_data is not None:
            input_prompt = build_example_prompt(
                input_label=properties["input_label"], 
                input_value=input_data[properties["input_column"]], 
                # output_label=properties["output_label"],
                is_example=False
            )
            prompt += [{
                "role": "user",
                "content": "Based on the API specifications and previous examples, " + properties["prediction_prompt"] + input_prompt[0]["content"]
            }]
    
    return prompt


def build_prompt(
    strategy: str,
    prompt_type: str = 'examples',
    input_data: object = None, 
    examples_df: pd.DataFrame = None, 
    examples_limit: int = 30,
    seed: int = 42,
    chat_format: bool = True,
    config_path: str = './config/prompts',
    flattened_prompt: bool = False
):
    if prompt_type == 'examples':
        messages = build_examples_prompt(strategy=strategy, examples_df=examples_df, input_data=input_data, limit=examples_limit, headless=False, seed=seed, config_path=config_path)
    elif prompt_type == 'apispec':
        messages = build_spec_prompt(strategy=strategy, input_data=input_data, examples_df=examples_df, examples_limit=examples_limit, seed=seed, config_path=config_path)
    
    if not chat_format:
        raise NotImplementedError("Not implemented yet")

    # prompt_length = measure_prompt_length(prompt)
    # print(f"Base prompt tokens length: {prompt_length}")

    if flattened_prompt:
        messages2 = []
        user_prompt = ''
        for message in messages:
            if message['role'] == 'system':
                messages2.append(message)
            elif message['role'] == 'user':
                user_prompt += message['content']
                user_prompt += '\n'
            elif message['role'] == 'assistant':
                if message['content'] != 'ok':
                    user_prompt += message['content']
                    user_prompt += '\n'
        messages2 += [{'role': 'user', 'content': user_prompt}]
        messages = messages2
    
    return messages


def load_strategies(filepath='./config/prompts/prompt_strategies.yml'):
    with open(filepath, 'r') as file:
        data = yaml.safe_load(file)
    return data


def measure_prompt_length(messages: list) -> int:
    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
    prompt_str = "\n".join([p['content'] for p in messages if p['role'] == 'user'])
    base_prompt_tokens_len = len(tokenizer(prompt_str, max_length=51200, truncation=True)["input_ids"])
    return base_prompt_tokens_len