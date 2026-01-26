from google.adk.agents import LlmAgent

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

# 3. Note: You need to put .env file only inside the root agent. You don't have to add it under other agents if you are creating multi agent system.