from config import HUGGING_FACE_KEY
from huggingface_hub import InferenceClient

print(HUGGING_FACE_KEY)
client = InferenceClient(
    provider="cerebras",
    api_key =HUGGING_FACE_KEY,
)

def generate_blog(title, transcript):
    prompt = f"""You are a professional content writer. Write a high-quality, SEO-optimized blog post.
Title: {title}
Transcript:
{transcript}
"""
    response = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    )
    return response.choices[0].message.content



