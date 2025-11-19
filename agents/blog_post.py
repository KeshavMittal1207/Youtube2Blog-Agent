import requests
from config import DEV_API_KEY


def post_blog_service(title:str , blog_draft : str):
    headers = {"api-key": DEV_API_KEY ,
                "Content-Type": "application/json"

               }
    data = {
        "article":  {
        "title": title,
        "body_markdown": blog_draft,
        "published": True,
        "series": "Agentic AI projects",
        # "main_image": "string",
        # "canonical_url": "string",
        "description": title,
        "tags": "blogging",
        # "organization_id": 0
        }
    }
    response = requests.post("https://dev.to/api/articles", json=data, headers=headers)
    if(response.status_code == 201):
        print("Blog Posted !")
    else:
        print("FAILED !!!")
        print("Status Code:", response.status_code)
