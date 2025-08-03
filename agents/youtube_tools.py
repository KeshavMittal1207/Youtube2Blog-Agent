from youtube_transcript_api import YouTubeTranscriptApi
import requests

def fetch_transcript(video_id: str):
    api = YouTubeTranscriptApi()
    transcript = api.fetch(video_id=video_id ,languages=["en"])
    return " ".join([t.text for t in transcript])

def fetch_title(video_id: str):
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
    response = requests.get(url)
    return response.json()["title"]