import asyncio
from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from dotenv import load_dotenv

from reminder_agent import agent
import utils


load_dotenv()

############
# Constants
############

APP_NAME = "Reminder App"
USER_ID = "v01"

async def main():
    try:

        ################################
        # Step1: Create Session Service
        ################################

        """
        sqlite:///./agent-sessions.db uses 'pysqlite' synchronous driver
        sqlite+aiosqlite:///./agent-sessions.db uses 'aiosqlite' driver

        sqlalchemy.exc.InvalidRequestError: The asyncio extension requires an async driver to be used. The loaded 'pysqlite' is not async.
        """

        db_url = "sqlite+aiosqlite:///./agent-sessions.db"
        session_service = DatabaseSessionService(db_url=db_url)

        ############################################################
        # Step2: Check if session already exists. If not create one.
        ############################################################

        existing_sessions = await session_service.list_sessions(app_name=APP_NAME, user_id=USER_ID)
        
        if existing_sessions.sessions:
            session_id = existing_sessions.sessions[0].id
        else:
            initial_state = {
                "user_name": "v01",
                "reminders": [],
            }
            session_id = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, state=initial_state)

        """
        sessions=[Session(id='51bd1e47-6aa3-4de6-aa80-3581c68680e3', app_name='Reminder App', user_id='v01', state={'user_name': 'v01', 'reminders': []}, events=[], last_update_time=1766670728.0)]
        """

        #########################
        # Step3: Create a runner
        #########################

        runner = Runner(
            agent=agent.root_agent,
            app_name=APP_NAME,
            session_service=session_service,
        )

        while True:
            prompt = input("you: ")

            if prompt.lower() in ["quit", "exit"]:
                exit(0)
            
            response = await utils.call_agent(
                runner=runner,
                session_id=session_id,
                query=prompt,
                user_id=USER_ID
            )

            print(response)

    except Exception as e:
        print(e)
    finally:
        # Shutsdown connection pool + aiosqlite worker thread
        if "session_service" in locals():
            await session_service.db_engine.dispose()

asyncio.run(main())