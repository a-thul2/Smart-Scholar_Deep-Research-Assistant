# Smart Scholar - Deep Research 🧠📚

**Smart Scholar** is an agentic deep-research assistant that coordinates multiple AI agents to plan searches, summarize findings, draft a detailed report, and sends the finished report via email. The project stitches together modular agents (Planner, Searcher, Writer, Emailer) orchestrated by a `ResearchManager` and exposes a simple Gradio UI for interactive use.

---

## 🚀 Features

* Planner Agent: generates targeted web search queries based on your research question.
* Search Agent: queries the web (via Serper API) and summarizes search results.
* Writer Agent: synthesizes a long, structured markdown report from search summaries (Gemini model).
* Email Agent: converts the report to HTML and sends it using SendGrid.
* Lightweight Gradio UI for interactive research sessions.

---

## 🌐 Live Demo (Hugging Face Spaces)

You can try **Smart Scholar – Deep Research** live via Hugging Face Spaces:

🔗 **Live Demo:**
👉 [Smart Scholar - Deep Research Agent]((https://huggingface.co/spaces/athul8/Deep-Research-Agent))

The demo provides the same end-to-end research workflow through a web interface, powered by the underlying agent architecture.

---

## ⚠️ Important Notes & Limitations

* The project currently uses the **Gemini API (Free Tier)**.
* Due to **API rate limits**, the following may occasionally occur:

  * The generated research report may be **incomplete**
  * The pipeline may **fail or stop midway**
* These issues are more likely when **multiple users access the Hugging Face Space simultaneously**, as free-tier API quotas are shared and limited.

💡 **Reason:**
Gemini free-tier APIs have strict request and token limits. When those limits are exceeded, responses may be truncated or requests may fail.

📌 **Recommendation:**
For stable and uninterrupted usage:

* Run the project **locally** with your own API keys
* Or upgrade to a **paid Gemini plan** if deploying for heavier or public usage

---

## 🔧 Quickstart

1. Clone the repository:

```bash
git clone https://github.com/a-thul2/Smart-Scholar_Deep-Research-Assistant.git
cd "Smart Scholar - Deep Research"
```

2. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
# On Windows
.\.venv\Scripts\activate
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and set the required environment variables.

```env
GEMINI_API_KEY=your_gemini_api_key
SERPER_API_KEY=your_serper_api_key
SENDGRID_API_KEY=your_sendgrid_api_key
FROM_EMAIL=your_verified_sendgrid_from_email
TO_EMAIL=recipient_email
```

4. Run the UI:

```bash
python deep_research.py
```

The Gradio UI will launch in your browser where you can enter a research query and run the pipeline.

---

## 📝 Notes

* `GEMINI_API_KEY` is used via the OpenAI-compatible `AsyncOpenAI` client configured to a Gemini base URL.
* `SERPER_API_KEY` is used for web search (Serper API).
* `SENDGRID_API_KEY`, `FROM_EMAIL`, and `TO_EMAIL` are required if you want the Email agent to send reports.

---

## 🏗 Architecture Overview

High-level flow:

1. **User** submits a query (Gradio or programmatic).
2. **PlannerAgent** produces a set of targeted search terms.
3. **SearchAgent** runs web searches (Serper) and summarizes results.
4. **WriterAgent** synthesizes a long, structured markdown report from search summaries.
5. **EmailAgent** optionally emails the report via SendGrid.
6. **ResearchManager** orchestrates the end-to-end process and yields progress updates.

Files of interest:

* `deep_research.py` — Gradio-backed demo UI
* `research_manager.py` — Orchestration logic
* `planner_agent.py`, `search_agent.py`, `writer_agent.py`, `email_agent.py` — Agent implementations

---

## ▶️ Programmatic Example

You can run the manager without the UI in an async environment:

```python
import asyncio
from research_manager import ResearchManager

async def run_query(q):
    async for chunk in ResearchManager().run(q):
        print(chunk)

asyncio.run(run_query("Best approaches to training Transformer models on small datasets"))
```

---

## 🧪 Development

* Use a virtualenv or conda environment and the `requirements.txt` file.
* Run linters/tests if present (add tests & CI as needed).
* The code uses `dotenv` to load `.env` values during development.
