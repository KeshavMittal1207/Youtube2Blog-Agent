from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel , Field
from agents.youtube_tools import fetch_transcript, fetch_title
from agents.blog_generator import generate_blog
from config import GEMINI_KEY
from typing import Literal, TypedDict
from agents.blog_post import post_blog_service

llm = ChatGoogleGenerativeAI(model = "gemini-2.5-pro" , api_key = GEMINI_KEY)

class EvaluationSchema(BaseModel):
    evaluation : Literal["needs_improvement" ,"approved"]
    feedback : str

class AgentState(TypedDict, total=False):
    video_id: str
    transcript: str
    evaluation : Literal["approved" , "needs_improvement"]
    feedback : str
    iteration : int
    max_iteration : int
    title: str
    blog_draft: str 

# STEP 1: Fetch YouTube transcript & title
def get_transcript_node(state: AgentState):
    title = fetch_title(state["video_id"])
    transcript = fetch_transcript(state["video_id"])
    return {**state, "transcript": transcript, "title": title}

# STEP 2: Generate blog from transcript
def generate_blog_node(state: AgentState):
    blog = generate_blog(state["title"], state["transcript"])
    return {**state, "blog_draft": blog}

# STEP 3: Evaluate blog 
def evaluate_blog_node(state: AgentState):
    prompt = f"""
    Evaluate this blog for clarity, structure, readability, SEO, engagement, and correctness.

    Blog:
    {state['blog_draft']}
    """
    structured_llm = llm.with_structured_output(EvaluationSchema)
    result = structured_llm.invoke(prompt)
    return {**state , 'evaluation':result.evaluation , 'feedback':result.feedback}

def route_evaluation(state):
    if state['evaluation'] == 'approved' or state['iteration'] >= state['max_iteration']:
        return 'approved'
    return 'needs_improvement'

# STEP 4: Optimize blog if needed
def optimize_blog_node(state: AgentState):
    prompt = f"""Improve this blog for clarity, SEO, storytelling, and accuracy:
    {state['blog_draft']}
    """
    optimized = llm.invoke(prompt).content
    return {**state , 'blog_draft': optimized , 'iteration': state['iteration'] + 1}

# STEP 5: Publish (manually called later)
def post_blog_node(state: AgentState):
    post_blog_service(state["title"] , state["blog_draft"])
    return state

# Build LangGraph workflow — ONLY generate + evaluate + improve
def build_generation_workflow():
    graph = StateGraph(AgentState)

    graph.add_node("get_transcript", get_transcript_node)
    graph.add_node("generate_blog", generate_blog_node)
    graph.add_node("evaluate_blog", evaluate_blog_node)
    graph.add_node("optimize_blog", optimize_blog_node)

    graph.add_edge(START , "get_transcript")
    graph.add_edge("get_transcript", "generate_blog")
    graph.add_edge("generate_blog" , "evaluate_blog")

    graph.add_conditional_edges(
        "evaluate_blog",
        route_evaluation,
        {
            'approved': END,
            'needs_improvement': 'optimize_blog'
        }
    )

    graph.add_edge("optimize_blog", "evaluate_blog")

    return graph.compile()

# SIMPLE publish function for Streamlit
def publish_blog(state: AgentState):
    return post_blog_node(state)
