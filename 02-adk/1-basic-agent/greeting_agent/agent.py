from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.models import Gemini

root_agent = Agent(
    name = "greeting_agent",
    model=Gemini(model="gemini-2.0-flash-lite-001"),
    # model=LiteLlm(model="gemini-2.0-flash-lite-001"), # https://docs.litellm.ai/docs/
    description="Greeting Agent",
    instruction="""
    You are a helpful assistant that greets the user. Ask for the user's name and greet them by name.
    """
)