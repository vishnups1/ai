from google.genai import types
from google.adk.runners import Runner

async def call_agent(runner: Runner, user_id, session_id, query):
    message = types.Content(role="user", parts=[types.Part(text=query)])

    events = runner.run_async(
        user_id = user_id,
        session_id = session_id,
        new_message = message,
    )

    async for event in events:
        if event.is_final_response():
            if event.content and event.content.parts and event.content.parts[0].text.strip():
                return event.content.parts[0].text
