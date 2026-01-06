from pydantic import BaseModel, Field
from agents import Agent
import asyncio
import os
from dotenv import load_dotenv
from agents import OpenAIChatCompletionsModel
from openai import AsyncOpenAI

load_dotenv(override=True)

gemini_api_key = os.getenv('GEMINI_API_KEY')

if not gemini_api_key:
    raise RuntimeError("GEMINI_API_KEY not set")

if not os.environ.get("SENDGRID_API_KEY"):
    raise RuntimeError("SENDGRID_API_KEY not set")


GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
gemini_client = AsyncOpenAI(base_url=GEMINI_BASE_URL, api_key=gemini_api_key)
gemini_model = OpenAIChatCompletionsModel(model="gemini-2.5-flash-lite", openai_client=gemini_client)

HOW_MANY_SEARCHES = 1

INSTRUCTIONS = f"You are a helpful research assistant. Given a query, come up with a set of web searches \
to perform to best answer the query. Output {HOW_MANY_SEARCHES} terms to query for."


class WebSearchItem(BaseModel):
    reason: str = Field(description="Your reasoning for why this search is important to the query.")
    query: str = Field(description="The search term to use for the web search.")


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(description="A list of web searches to perform to best answer the query.")
    
planner_agent = Agent(
    name="PlannerAgent",
    instructions=INSTRUCTIONS,
    model=gemini_model,
    output_type=WebSearchPlan,
)