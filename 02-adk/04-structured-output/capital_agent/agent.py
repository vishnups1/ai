from google.adk.agents import LlmAgent

INSTRUCTION="""
You are a helpful assistant. Given a country name you return the capital of that country.
"""

from pydantic import BaseModel, Field

class CapitalOutput(BaseModel):
    capital: str = Field(description="The capital of the country")

############################################################
# Use of output schema disables agents ability to use tools
############################################################

root_agent = LlmAgent(
    name="capital_agent",
    description="Capital Agent",
    instruction=INSTRUCTION,
    output_schema=CapitalOutput,
    output_key="found_capital" # store result in state['found_capital']
)