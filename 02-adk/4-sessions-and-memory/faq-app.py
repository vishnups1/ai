from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

from google.adk.events import event

from google.genai import types
from uuid import uuid4
from dotenv import load_dotenv

from faq_agent.faq_agent import faq_agent

load_dotenv()

session_service=InMemorySessionService()

runner=Runner(
    agent=faq_agent,
    app_name="faq-app",
    session_service=session_service,
)

async def create_session(user_id: str):

    session_id=str(uuid4())

    await session_service.create_session(
        app_name="faq-app",
        session_id=session_id,
        user_id=user_id,
        state={}
    )

    return session_id

if __name__ == "__main__":
    import asyncio
    
    async def main():
        user_id="vishnu01"
        session_id=await create_session(user_id)

        new_message=types.Content(
            role="user",
            parts=[types.Part(text="hi there!")]
        )

        # runner.run returns a Generator
        # events is a Generator
        events=runner.run(user_id=user_id, session_id=session_id, new_message=new_message)

        # Agent actually runs here
        for event in events:
            # print(event.model_dump_json())
            if event.is_final_response() and event.content:
                for part in event.content.parts:
                    pass
                    # print(part.text)

        """
            {
                "model_version": "gemini-2.5-flash",
                "content": {
                    "parts": [
                        {
                            "media_resolution": null,
                            "code_execution_result": null,
                            "executable_code": null,
                            "file_data": null,
                            "function_call": null,
                            "function_response": null,
                            "inline_data": null,
                            "text": "Hello! How can I help you today? Feel free to ask me any questions you have.",
                            "thought": null,
                            "thought_signature": null,
                            "video_metadata": null
                        }
                    ],
                    "role": "model"
                },
                "grounding_metadata": null,
                "partial": null,
                "turn_complete": null,
                "finish_reason": "STOP",
                "error_code": null,
                "error_message": null,
                "interrupted": null,
                "custom_metadata": null,
                "usage_metadata": {
                    "cache_tokens_details": null,
                    "cached_content_token_count": null,
                    "candidates_token_count": 19,
                    "candidates_tokens_details": [
                        {
                            "modality": "TEXT",
                            "token_count": 19
                        }
                    ],
                    "prompt_token_count": 63,
                    "prompt_tokens_details": [
                        {
                            "modality": "TEXT",
                            "token_count": 63
                        }
                    ],
                    "thoughts_token_count": 19,
                    "tool_use_prompt_token_count": null,
                    "tool_use_prompt_tokens_details": null,
                    "total_token_count": 101,
                    "traffic_type": "ON_DEMAND"
                },
                "live_session_resumption_update": null,
                "input_transcription": null,
                "output_transcription": null,
                "avg_logprobs": -0.4098720048603259,
                "logprobs_result": null,
                "cache_metadata": null,
                "citation_metadata": null,
                "interaction_id": null,
                "invocation_id": "e-fc548ce9-63de-4e23-b375-864e013bc2a8",
                "author": "faq_agent",
                "actions": {
                    "skip_summarization": null,
                    "state_delta": {},
                    "artifact_delta": {},
                    "transfer_to_agent": null,
                    "escalate": null,
                    "requested_auth_configs": {},
                    "requested_tool_confirmations": {},
                    "compaction": null,
                    "end_of_agent": null,
                    "agent_state": null,
                    "rewind_before_invocation_id": null
                },
                "long_running_tool_ids": null,
                "branch": null,
                "id": "2e786db9-aab8-42b0-aa6b-5f09bc5f19c9",
                "timestamp": 1766596270.61928
            }
        """

        session_history=await session_service.get_session(session_id=session_id,app_name="faq-app",user_id="vishnu01")

        print(session_history.model_dump_json())

        # Debug:
        # events=list(runner.run(user_id=user_id, session_id=session_id, new_message=new_message))
        # print(len(events))
        # print(events)

        # event=events.__next__()
        # print(event)
    
    asyncio.run(main())
