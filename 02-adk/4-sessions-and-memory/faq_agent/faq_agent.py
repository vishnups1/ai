from google.adk.agents import Agent
# from google.adk.models import Gemini

faq_agent = Agent(
    name="faq_agent",
    description="An agent that answers frequently asked questions",
    instruction="You are a helpful FAQ assistant. Answer user questions clearly and concisely based on common inquiries. If you don't know the answer, politely say so.",
    model="gemini-2.5-flash"
)