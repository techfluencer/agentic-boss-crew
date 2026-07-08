# 🦁 agentic-boss-crew — a hierarchical CrewAI team

Build an AI **crew with a boss**. A manager agent (the Lion) breaks a request into
tasks and **delegates** each one to the right specialist — an Architect, an Engineer,
and a Reviewer — then delivers a finished, reviewed result.

> Lesson 2 of the CrewAI series on **[@techfluencer-eval](https://www.youtube.com/@techfluencer-eval)**.
> Lesson 1 (a sequential crew): https://github.com/techfluencer/crewai-first-crew

---

## 🧠 What it builds

The crew writes and reviews a Python function `is_palindrome(text)` (ignoring case,
spaces, and punctuation) — but the point isn't the function, it's **how the crew works**:

| Agent | Role | Job |
|-------|------|-----|
| 🦁 **Lion** | Engineering Manager | Plans, **delegates**, and decides when it's done |
| 🦉 **Owl** | Software Architect | Designs the approach (signature, steps, edge cases) |
| 🦫 **Beaver** | Python Engineer | Writes the implementation |
| 🐈 **Cat** | Code Reviewer | Hunts bugs & missed edge cases, returns the final code |

**Sequential vs hierarchical:** in Lesson 1 *you* set the order. Here, `Process.hierarchical`
hands control to the manager (`manager_agent`) — it decides who works, in what order, and
when the job is truly done.

## 💡 The real lesson: give the *boss* the strongest model

Counter-intuitively, the manager does the **hardest reasoning** in the crew (decompose the
goal, pick the right specialist, format each delegation exactly, judge "done"). On a small
model it can loop and hit `Maximum iterations reached`. The fix:

```python
manager_llm = LLM(model="azure/gpt-4.1")          # best model for the boss
manager = Agent(role="Engineering Manager (the Lion)", ..., llm=manager_llm)
# specialists stay on the cheaper azure/gpt-4o-mini — focused jobs, cheaper is fine

Best model where the thinking is hardest; cheaper models for the focused work — smarter and cheaper.

🚀 Setup & run
Uses uv and Azure OpenAI (works with any provider — just change the model strings).

uv sync                       # install dependencies
cp .env.example .env          # then add your Azure OpenAI key + endpoint
uv run python main.py

.env (see .env.example):

AZURE_API_KEY=your-key-here
AZURE_API_BASE=https://YOUR-RESOURCE.openai.azure.com/
AZURE_API_VERSION=2024-08-01-preview

🧩 Requirements
Python ≥ 3.11 · crewai (with the azure-ai-inference extra) · an LLM endpoint
📺 Watch the lesson
Full walkthrough — building it, running it, and debugging the delegation loop:
▶ CrewAI Lesson 2: The Boss Agent 

Here is the youtube video link : 
https://youtu.be/_sdrtKAeh24

⭐ Star the repo if it helped, and subscribe for a new hands-on AI-agent lesson each week.

