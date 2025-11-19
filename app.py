import streamlit as st
from workflow import build_generation_workflow,publish_blog
from agents.youtube_tools import fetch_title, fetch_transcript

st.set_page_config(page_title="YouTube → Blog Generator", layout="wide")

st.title("📺 YouTube → 📝 Blog Generator (LangGraph + Streamlit)")
st.write("Generate, optimize, evaluate, and publish blog posts from YouTube videos.")

# --- USER INPUT FORM ---
st.header("📥 Enter YouTube Video ID")
video_id = st.text_input("YouTube Video ID", placeholder="e.g., dQw4w9WgXcQ")

# A session state to store workflow state between steps
if "state" not in st.session_state:
    st.session_state.state = None
if "graph" not in st.session_state:
    st.session_state.graph = build_generation_workflow()

if st.button("Generate Blog") and video_id.strip():
    with st.spinner("Generating blog..."):
        initial_state = {
            "video_id": video_id.strip(),
            "iteration": 1,
            "max_iteration": 5
        }
        # Run only the generation/eval loop — returns when evaluation == approved or max_iteration reached
        result = st.session_state.graph.invoke(initial_state)
        st.session_state.state = result

st.divider()


# --- SHOW BLOG DRAFT ---
if st.session_state.state:
    state = st.session_state.state

    st.subheader("Generated Title")
    st.write(state.get("title", "— No title generated yet —"))

    st.subheader("Blog Draft")
    st.text_area("Draft", value=state.get("blog_draft",""), height=400)

    st.subheader("💬 Evaluation")
    st.write(f"**Status:** {state['evaluation'].upper()}")

    st.divider()

    if st.button("Publish Blog"):
        st.session_state.show_confirm = True

    if st.session_state.get("show_confirm", False):
        st.warning("Are you sure you want to publish this blog?")
        col1, col2 = st.columns(2)

        with col1:
            yes = st.button("✅ Yes, Publish Now")

        with col2:
            no = st.button("❌ No, Cancel")

        if yes:
            publish_blog(state)   # <--- your function
            st.success("Blog posted successfully!")
            st.session_state.show_confirm = False

        if no:
            st.info("Publishing canceled.")
            st.session_state.show_confirm = False
    
    if state.get("posted"):
        st.info("This draft has been posted.")
