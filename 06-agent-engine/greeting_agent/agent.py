from google.adk.agents import LlmAgent
from google.cloud.aiplatform_v1.types import reasoning_engine
from vertexai.agent_engines import AdkApp

INSTRUCTION = """
You are a helpful assistant that greets the user. Ask for the user's name and greet them by name.
"""

# 1. Inside adk you need to make sure you have atleast one root agent
root_agent = LlmAgent(
    # 2. Name of the agent should match the directory
    name="greeting_agent",
    # https://ai.google.dev/gemini-api/docs/modles
    model="gemini-2.0-flash",
    description="Greeting agent",
    instruction=INSTRUCTION
)

app = AdkApp(agent=root_agent)
