# 🧠🎥 YouTube-to-Blog: Agentic AI Workflow with LangGraph
Transform **YouTube videos into polished, SEO-friendly blog posts** with a fully autonomous Agentic AI workflow powered by LangGraph and LangChain.

This project showcases how AI agents can autonomously:
- Fetch video transcripts and titles from YouTube
- Generate high-quality blog drafts
- Offer a revision feedback loop
- Post directly to a blogging platform (Dev.to)

---

## 🚀 What It Does

> A single YouTube video ➝ a full blog article in a minute.

### ✨ Features
- 📺 Extracts video title and transcript automatically
- ✍️ Uses LLMs (e.g. LLaMA 3) to write long-form, structured content
- 🔁 Human-in-the-loop: Revise, accept, or abort generated drafts
- 🚀 Publishes blog to Dev.to via API
- 🧠 Built with LangGraph’s state machine orchestration

---

## 🧱 Project Structure
  youtube-blog-agent/
  ├── agents/
  │ ├── youtube_tools.py # Fetches YouTube data
  │ ├── blog_generator.py # LLM-based blog generation
  │ └── revision_agent.py # Handles revision instructions
  ├── workflow.py # LangGraph state machine
  ├── main.py # Entry point
  ├── config.py # API keys and config loader
  ├── requirements.txt
  ├── .env.example # Environment variable template
  └── README.md

