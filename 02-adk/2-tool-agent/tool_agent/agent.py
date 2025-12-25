from google.adk import Agent
from google.adk.models import Gemini
from google.adk.tools import google_search
from datetime import datetime, timezone

def get_current_time() -> dict:
    return {"current_time": f"${datetime.now(tz=timezone.utc)}"}

root_agent = Agent(
    name="tool_agent",
    model=Gemini(model="gemini-2.0-flash-lite-001"),
    description="Tool Agent",
    instruction="""
    You are a friendly assistant. You use below tools.
    - # google_search
    - get_current_time
    """,
    # tools=[google_search]
    tools=[get_current_time]
)
