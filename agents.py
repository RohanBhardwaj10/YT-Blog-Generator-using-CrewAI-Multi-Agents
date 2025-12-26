from crewai import Agent
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("❌ key not found in environment variables.")


blog_researcher = Agent(
    role="YouTube Blog Researcher",
    goal="Find and summarize insights from YouTube videos about {topic}.",
    verbose=False,
    memory=True,
    backstory=(
        "A research assistant specialized in analyzing YouTube videos "
        "and extracting key insights about technology, AI, and trending topics."
    ),
    allow_delegation=False,
    llm="gpt-4o-mini"  # ✅ Lightweight, fast, OpenAI model
)

blog_writer = Agent(
    role="Technical Blog Writer",
    goal="Write an engaging, clear blog post about {topic} using the research data.",
    verbose=False,
    memory=True,
    backstory=(
        "A creative content writer skilled in crafting engaging and easy-to-read blogs "
        "based on technical or research information."
    ),
    allow_delegation=False,
    llm="gpt-4o-mini"

)
