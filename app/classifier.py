import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")


def model_pipeline(prompt: str, image_str: str):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    payload = {
        "model": "gpt-4-turbo",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_str}"},
                    },
                ],
            }
        ],
        "max_tokens": 1000,
    }
    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )
    response_json = response.json()["choices"][0]["message"]["content"]
    json_str = response_json.split("```json\n")[1].split("\n```")[0]
    json_data = json.loads(json_str)
    return json_data
