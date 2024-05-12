import requests 
from datetime import datetime
import os
import pickle
import json
from json.decoder import JSONDecodeError


class TogetherAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        
    def chat_complete(self, messages, model_name, n=100, max_tokens=512, temperature=1.0, top_p=0.7, top_k=50, serialize_id=None, serialize_path=None):
        url = "https://api.together.xyz/v1/chat/completions"

        payload = {
            "model": model_name,
            "messages": messages,
            "max_tokens": max_tokens,
            "stop": ["</s>"],
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "repetition_penalty": 1,
            "n": n,
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        response = requests.post(url, json=payload, headers=headers)

        if serialize_path is not None:
            current_time = datetime.now()
            timestamp = current_time.strftime("%Y-%m-%d_%H-%M-%S")
            file_name = f"{serialize_id}_n{n}_{timestamp}.pkl"
            file_path = os.path.join(serialize_path, file_name)
            os.makedirs(serialize_path, exist_ok=True)
            with open(file_path, 'wb') as file:
                pickle.dump(response, file)

        try:
            json_response = json.loads(response.text)
        except JSONDecodeError as e:
            print(f"Failed to parse response:")
            print(response.text)
            print(e)
            raise e
        except Exception as e:
            print("Failed to execute request")
            print(e)
            raise e

        return json_response    