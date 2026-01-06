from agents import Agent, WebSearchTool, ModelSettings
import asyncio
import os
from dotenv import load_dotenv
from agents import OpenAIChatCompletionsModel
from openai import AsyncOpenAI
import requests
from typing import Dict
from agents import Agent, Tool, ModelSettings, function_tool

load_dotenv(override=True)

gemini_api_key = os.getenv('GEMINI_API_KEY')

if not gemini_api_key:
    raise RuntimeError("GEMINI_API_KEY not set")

if not os.environ.get("SENDGRID_API_KEY"):
    raise RuntimeError("SENDGRID_API_KEY not set")


GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
gemini_client = AsyncOpenAI(base_url=GEMINI_BASE_URL, api_key=gemini_api_key)
gemini_model = OpenAIChatCompletionsModel(model="gemini-2.5-flash-lite", openai_client=gemini_client)


SERPER_API_KEY = os.getenv("SERPER_API_KEY")

@function_tool
def serper_search(query: str) -> str:
    url = "https://google.serper.dev/search"
    payload = {
        "q": query,
        "num": 3
    }
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers, timeout=15)
    response.raise_for_status()

    data = response.json()

    snippets = []

    for item in data.get("organic", []):
        title = item.get("title", "")
        snippet = item.get("snippet", "")
        link = item.get("link", "")
        snippets.append(f"{title}: {snippet}")

    return "\n".join(snippets)


INSTRUCTIONS = (
    "You are a research assistant. Given a search term, you search the web for that term and "
    "produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300 "
    "words. Capture the main points. Write succintly, no need to have complete sentences or good "
    "grammar. This will be consumed by someone synthesizing a report, so its vital you capture the "
    "essence and ignore any fluff. Do not include any additional commentary other than the summary itself."
)

search_agent = Agent(
    name="Search agent",
    instructions=INSTRUCTIONS,
    tools=[serper_search],
    model=gemini_model,
    model_settings=ModelSettings(tool_choice="required"),
)
