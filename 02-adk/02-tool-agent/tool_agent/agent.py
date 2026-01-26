from google.adk.agents import LlmAgent
from google.adk.tools.google_search_tool import google_search

INSTRUCTION = """
You are a helpful assistant that can use the following tools:
- google_search
- current_date_time
"""

from typing import Dict
from datetime import datetime, timezone, date

# https://google.github.io/adk-docs/tools-custom/function-tools/#function-tool

"""
[user]: what's the response type of tool current_date_time tool?
[tool_agent]: The response type of the `current_date_time` tool is a dictionary.
"""

def current_date_time() -> Dict:
    """
    Returns the current date and time 
    
    Args:
      None
    """

    return {
        "time": datetime.now(timezone.utc).isoformat(),
        "date": date.today().isoformat(),
    }

root_agent = LlmAgent(
    name="tool_agent",
    # https://ai.google.dev/gemini-api/docs/modles
    model="gemini-2.0-flash",
    description="Tool",
    instruction=INSTRUCTION,
    # tools=[google_search, current_date_time] # THIS WONT WORK: Multiple tools are supported only when they are all search tools.
    tools=[current_date_time]
)