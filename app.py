import streamlit as st
from crewai import Crew, Process
from agents import blog_researcher, blog_writer
from tasks import research_task, write_task
from tools import get_youtube_tool
from dotenv import load_dotenv
import os
import requests
import re

load_dotenv()

st.set_page_config(page_title="AI Blog Generator", page_icon="📝", layout="centered")
st.title("🎥 YT Blog Generator using Crew AI")

def resolve_channel_url(input_str: str):
    input_str = input_str.strip()

    if input_str.startswith("http"):
        return input_str

    if input_str.startswith("UC"):
        return f"https://www.youtube.com/channel/{input_str}"

    if input_str.startswith("@"):
        try:
            handle = input_str[1:]
            url = f"https://www.youtube.com/@{handle}"
            response = requests.get(url)
            match = re.search(r'"channelId":"(UC[\w-]{22})"', response.text)
            if match:
                return f"https://www.youtube.com/channel/{match.group(1)}"
            else:
                st.warning(f"⚠️ Could not resolve handle `{input_str}` to a valid channel ID.")
                return None
        except Exception as e:
            st.error(f"Error resolving channel: {e}")
            return None

    return f"https://www.youtube.com/@{input_str}"

channel_handle = st.text_input("Enter YouTube channel handle or URL :", placeholder="@IBMTechnology or https://youtube.com/@IBMTechnology")
topic = st.text_input("Enter your blog topic:", placeholder="e.g., What is AI & ML?")

if st.button("Generate Blog"):
    if topic.strip():
        with st.spinner("Generating blog..."):
            resolved_url = resolve_channel_url(channel_handle)
            if not resolved_url:
                st.error("Could not resolve the YouTube channel. Try a different handle or paste a channel ID (UC...).")
            else:
                yt_tool = get_youtube_tool(resolved_url)

                crew = Crew(
                    agents=[blog_researcher, blog_writer],
                    tasks=[research_task, write_task],
                    process=Process.sequential,
                    memory=True,
                    cache=True,
                    tools=[yt_tool] if yt_tool else []
                )

                result = crew.kickoff(inputs={'topic': topic})
                st.subheader("📝 Generated Blog:")
                if isinstance(result, dict):
                    if "raw" in result:
                        st.markdown(result["raw"], unsafe_allow_html=True)
                    else:
                        st.write(result)
                else:
                    st.markdown(str(result), unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please enter a topic.")
