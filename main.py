# main.py
from workflow import build_workflow

if __name__ == "__main__":
    video_id = input("\n Enter YouTube video ID: ").strip()
    print(video_id)
    state = {"video_id": video_id}
    print(state)
    graph = build_workflow()
    result = graph.invoke(state)

    print("\n Done. Final state:")
    print(result)
