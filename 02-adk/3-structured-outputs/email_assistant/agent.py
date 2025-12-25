from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field

class EmailSchema(BaseModel):
    subject: str = Field(description="The subject line of the email.")
    body: str = Field(description="The body of the email.")

root_agent = LlmAgent(
    name="email_assistant",
    model="gemini-2.0-flash-lite-001",
    instruction="""
        You are an Email Generation Assistant.
        Your task is to generate a professional email based on the user's request.

        GUIDELINES:
        - Create an appropriate subject line (Concise and Relevant)
        - Write a well-structured body with:
            * Professional greeting
            * Clear and Concise main content
            * Appropriate closing
            * You name as signature
        - Suggest relevant attachments if applicable (empty list if none needed)
        - Email tone should match the purpose (Formal for business and Friendly for colleagues)
        - Keep emails concise but complete

        IMPORTANT: Your response MUST be a valid JSON matching below structure
        {
            "subject": "Subject line here",
            "body": "Body here with proper paragraphs and formatting",
        }

        DO NOT include any explanations or additional text outside the JSON response.
    """,
    description="Generates professional emails with structured subject and body",
    output_key="email",
    output_schema=EmailSchema,
)