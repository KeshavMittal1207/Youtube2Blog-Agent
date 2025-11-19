# main.py
from workflow import build_workflow
from fastapi import FastAPI

app = FastAPI()

@app.post("/generate-blog")
def generate_blog_endpoint(video_id: str):
    graph = build_workflow()
    initial_state = {
        "video_id": video_id,
        "iteration": 1,
        "max_iteration": 5
    }
    result = graph.invoke(initial_state)
    return {
        "title": result["title"],
        "blog_draft": result["blog_draft"],
        "evaluation": result["evaluation"],
        "feedback": result["feedback"]
    }

    