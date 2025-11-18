import os
import requests
from dotenv import load_dotenv
from crewai_tools import YoutubeChannelSearchTool

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("❌ key not found in environment variables.")


def resolve_channel_url(channel_handle: str) -> str:
    """
    Converts a handle (@something) or channel ID (UC...) into a valid YouTube channel URL
    that CrewAI can use.
    """
    channel_handle = channel_handle.strip()

    if channel_handle.startswith("http"):
        return channel_handle

    if channel_handle.startswith("UC"):
        return f"https://www.youtube.com/channel/{channel_handle}"

    if channel_handle.startswith("@"):
        handle = channel_handle[1:]
    else:
        handle = channel_handle

    try:
        response = requests.get(f"https://www.youtube.com/@{handle}")
        html = response.text
        import re
        match = re.search(r"\/channel\/(UC[\w-]+)", html)
        if match:
            channel_id = match.group(1)
            print(f" Resolved handle @{handle} → Channel ID: {channel_id}")
            return f"https://www.youtube.com/channel/{channel_id}"
    except Exception as e:
        print(f"⚠Error resolving handle @{handle}: {e}")

    print(f"Could not resolve handle @{handle}, using direct handle URL.")
    return f"https://www.youtube.com/@{handle}"


def get_youtube_tool(channel_handle: str):
    """
    Initializes the YouTube Channel Search Tool with a valid URL.
    """
    if not channel_handle.strip():
        return None

    channel_url = resolve_channel_url(channel_handle)
    print(f"🔗 Final resolved URL: {channel_url}")

    try:
        yt_tool = YoutubeChannelSearchTool(youtube_channel_handle=channel_url)
        print(" YouTube Tool created successfully!")
        return yt_tool
    except Exception as e:
        print(f"Error initializing YouTube tool: {e}")
        return None
