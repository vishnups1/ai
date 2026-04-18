import os
import asyncio
from uuid import uuid4

from dotenv import load_dotenv

from agents import root_agent
from google.genai import types
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

load_dotenv()

APP_NAME = "customer_support_app"

async def main():

    # 1.Create an In-Memory session service
    session_service_stateful = InMemorySessionService()

    user_id = str(os.getenv(key="USER"))

    # 2.Create a session
    session = await session_service_stateful.create_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=str(uuid4()),
        state={
            "user_id": user_id,
            "user_preferences": {}
        }
    )

    # 3.Create a runner
    runner = Runner(
        app_name=APP_NAME,
        session_service=session_service_stateful,
        agent=root_agent,
    )

    while True:
        prompt = input(f"[{user_id}]: ")

        if prompt in ['exit', 'quit']:
            break

        # 4. Take the message from the user and convert it in to GenAI message type
        new_message = types.Content(
            role="user",
            parts=[types.Part(text=prompt)]
        )

        # 5. Process the prompt
        # It returns an async generator object, which is also an async iterator, implementing __aiter__() and __anext__()
        #
        # 1. gen = runner.run_async(...)
        # 2. iterator = gen.__aiter__()
        # 3. while True:
        #      try:
        #        event = await iterator.__anext__()
        #      except StopAsyncIteration:
        #        break
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session.id,
            new_message=new_message,
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    print(f"[agent]: {event.content.parts[0].text}")

if __name__ == "__main__":
    asyncio.run(main())
