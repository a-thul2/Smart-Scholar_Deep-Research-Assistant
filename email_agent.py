import os
from typing import Dict

import sendgrid
from sendgrid.helpers.mail import Email, Mail, Content, To
from agents import Agent, function_tool

import asyncio
import os
from dotenv import load_dotenv
from agents import OpenAIChatCompletionsModel
from openai import AsyncOpenAI

load_dotenv(override=True)

gemini_api_key = os.getenv('GEMINI_API_KEY')
from_base_email = os.getenv('FROM_EMAIL')
to_base_email = os.getenv('TO_EMAIL')

if not gemini_api_key:
    raise RuntimeError("GEMINI_API_KEY not set")

if not os.environ.get("SENDGRID_API_KEY"):
    raise RuntimeError("SENDGRID_API_KEY not set")


GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
gemini_client = AsyncOpenAI(base_url=GEMINI_BASE_URL, api_key=gemini_api_key)
gemini_model = OpenAIChatCompletionsModel(model="gemini-2.5-flash-lite", openai_client=gemini_client)


@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """Send an email with the given subject and HTML body"""
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get("SENDGRID_API_KEY"))
    from_email = Email(from_base_email)  # put your verified sender here
    to_email = To(to_base_email)  # put your recipient here
    content = Content("text/html", html_body)
    mail = Mail(from_email, to_email, subject, content).get()
    response = sg.client.mail.send.post(request_body=mail)
    print("Email response", response.status_code)
    return "success"


INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report. You should use your tool to send one email, providing the 
report converted into clean, well presented HTML with an appropriate subject line."""

email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model=gemini_model,
)
