from google.adk.agents import LlmAgent

root_agent = LlmAgent(
    name="customer_support_agent",
    model="gemini-2.0-flash",
    description="customer support agent",
    instruction="""
    You are a helpful assistant that handles customer queries

    Here are some information about the user:
    Name: {user_id}
    Preferences: {user_preferences}
"""
)