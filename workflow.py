from langgraph.graph import StateGraph
from agents.youtube_tools import fetch_transcript, fetch_title
from agents.blog_generator import generate_blog
from agents.revision_agent import revise_blog
from typing import TypedDict
from config import DEV_API_KEY
import requests

class AgentState(TypedDict):
    video_id: str
    transcript: str
    title: str
    blog_draft: str 

# STEP 1: Fetch YouTube transcript & title
def get_transcript_node(state):
    video_id = state["video_id"]
    title = fetch_title(video_id)
    transcript = fetch_transcript(video_id)
    return {**state, "transcript": transcript, "title": title}

# STEP 2: Generate blog from transcript
def generate_blog_node(state):
    print("Inside Blog function")
    blog = generate_blog(state["title"], state["transcript"])
    print(blog)
    return {**state, "blog_draft": blog}

# STEP 3: Ask human for confirmation
def human_confirmation_node(state):
    print("\n--- Blog Draft ---\n")
    print(state["blog_draft"])
    print("\n------------------\n")
    decision = input("Do you want to post this? (yes / revise / abort): ").strip().lower()
    return {"decision": decision}

# STEP 4: Handle blog revisions
def revise_blog_node(state):
    instructions = input("Enter revision instructions: ")
    revised = revise_blog(state["blog_draft"], instructions)
    return {**state, "blog_draft": revised}

def yes_blog_node(state):
    return {**state, "status": "accepted"}

def abort_blog_node(state):
    return {**state, "status": "aborted"}

def post_blog_node(state):
    print("Inside post blog node")
    print("Blog Posted")
    headers = {"api-key": DEV_API_KEY ,
                "Content-Type": "application/json"

               }
    data = {
        "article":  {
        "title": state["title"],
        "body_markdown": state["blog_draft"],
        "published": True,
        "series": "Agentic AI projects",
        # "main_image": "string",
        # "canonical_url": "string",
        "description": state["title"],
        "tags": "blogging",
        # "organization_id": 0
        }
    }
    print(data)
    response = requests.post("https://dev.to/api/articles", json=data, headers=headers)
    if(response.status_code == 201):
        print("Blog Posted")
    else:
        print("FAILED !!!")
        print("Status Code:", response.status_code)

    return {**state, "post_status": response.status_code}

# Build LangGraph workflow
def build_workflow():
    graph = StateGraph(AgentState)

    graph.add_node("get_transcript", get_transcript_node)
    graph.add_node("generate_blog", generate_blog_node)
    graph.add_node("human_confirmation", human_confirmation_node)
    graph.add_node("revise_blog", revise_blog_node)
    graph.add_node("abort_blog",abort_blog_node)
    graph.add_node("post_blog", post_blog_node)

    # Define graph structure
    graph.set_entry_point("get_transcript")
    graph.add_edge("get_transcript", "generate_blog")
    graph.add_edge("generate_blog", "human_confirmation")
    graph.add_edge("revise_blog","human_confirmation")

    graph.add_conditional_edges("human_confirmation", {
        "yes": post_blog_node,     
        "revise": revise_blog_node,
        "abort": abort_blog_node

    })

    graph.set_finish_point("post_blog")  
    return graph.compile()
