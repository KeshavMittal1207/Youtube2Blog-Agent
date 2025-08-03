
import requests
from config import HUGGING_FACE_KEY

API_URL = "https://router.huggingface.co/v1"
headers = {
    "Authorization": f"Bearer {HUGGING_FACE_KEY}"
}

def revise_blog(draft, instructions):
    prompt = f"""Revise the following blog post based on the instructions.

Blog Post:
{draft}

Instructions:
{instructions}
"""
    payload = {
        "model": "deepseek-ai/DeepSeek-R1",  #
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 700
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"Failed to call inference API: {response.status_code} {response.text}")
    
    return response.json()["choices"][0]["message"]["content"]

