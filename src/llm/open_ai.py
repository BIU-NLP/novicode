import openai
from datetime import datetime
import os
import pickle
import json
from json.decoder import JSONDecodeError


class OpenAIAPI:
    def __init__(self, organization: str, api_key: str):
        self.organization = organization
        self.api_key = api_key
        
    def chat_complete(self, messages, model_name, n=100, max_tokens=512, temperature=1.0, top_p=0.7, top_k=50, serialize_id=None, serialize_path=None):
        payload = {
            "model": model_name,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "n": n,
        }

        openai.organization = self.organization
        openai.api_key = self.api_key
        response = openai.chat.completions.create(**payload)

        if serialize_path is not None:
            current_time = datetime.now()
            timestamp = current_time.strftime("%Y-%m-%d_%H-%M-%S")
            file_name = f"{serialize_id}_n{n}_{timestamp}.pkl"
            file_path = os.path.join(serialize_path, file_name)
            os.makedirs(serialize_path, exist_ok=True)
            with open(file_path, 'wb') as file:
                pickle.dump(response, file)
                # print(f"Response serialized to {file_path}")

        return response    