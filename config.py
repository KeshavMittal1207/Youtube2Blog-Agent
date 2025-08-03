import os
from dotenv import load_dotenv

load_dotenv()

DEV_API_KEY=os.getenv("DEV_API_KEY") 
HUGGING_FACE_KEY=os.getenv("HUGGING_FACE_KEY")
print(HUGGING_FACE_KEY)
