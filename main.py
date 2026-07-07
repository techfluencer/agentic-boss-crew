from dotenv import load_dotenv

from crewai import Agent, Task, Crew, Process, LLM

load_dotenv()

# One shared brain (Azure OpenAI) for the whole crew.
# Reads AZURE_API_KEY / AZURE_API_BASE / AZURE_API_VERSION from .env
llm = LLM(model="azure/gpt-4o-mini")

# ---------------------------------------------------------------------------
# The specialists: three agents — each with a role, a goal, and a backstory.
# ---------------------------------------------------------------------------

architect = Agent(
    role="Software Architect (the Owl)",
    goal="Design a clean, simple approach for: {feature}",
    backstory=(
        "A wise owl who always plans before a single line is written. "
        "You outline the function signature, the steps, and the edge cases — but you write NO code."
    ),
    llm=llm,
    allow_delegation=False,
    verbose=True,
)

engineer = Agent(
    role="Python Engineer (the Beaver)",
    goal="Turn the architect's plan into correct, readable Python for: {feature}",
    backstory=(
        "A tireless builder who turns a plan into working code with a short docstring "
        "and no unnecessary cleverness."
    ),
    llm=llm,
    allow_delegation=False,
    verbose=True,
)

reviewer = Agent(
    role="Code Reviewer (the Cat)",
    goal="Catch bugs and missed edge cases, then return the final improved Python for: {feature}",
    backstory=(
        "A sharp-eyed critic who mentally tests the code, fixes what's weak, "
        "and hands back the polished final version."
    ),
    llm=llm,
    allow_delegation=False,
    verbose=True,
)

# ---------------------------------------------------------------------------
# The BOSS: a manager agent that plans, delegates, and decides when it's done.
# ---------------------------------------------------------------------------

manager_llm = LLM(model="azure/gpt-4.1")     # the boss does the hardest reasoning
                                             # so give it a stronger brain
manager = Agent(
    role="Engineering Manager (the Lion)",
    goal=(
        "Break the request into the right tasks, delegate each to the best specialist, "
        "and deliver a finished, reviewed solution for: {feature}"
    ),
    backstory=(
        "A calm, decisive lion who runs the team. You never write code yourself — "
        "you decide who works, in what order, and whether the result is truly done."
    ),
    llm=manager_llm,
    allow_delegation=True,
    verbose=True,
)

# ---------------------------------------------------------------------------
# The tasks: describe the WORK, not who does it. In a hierarchical crew the
# manager reads each task and assigns it to the right specialist.
# ---------------------------------------------------------------------------

design_task = Task(
    description=(
        "Design the solution for: {feature}. "
        "List the function signature, the numbered steps, and at least three edge cases. "
        "Do NOT write the implementation yet."
    ),
    expected_output="A short design: the signature, numbered steps, and a bullet list of edge cases.",
)

build_task = Task(
    description="Using the design, write the Python implementation for: {feature}.",
    expected_output="A single Python code block with the function and a short docstring.",
)

review_task = Task(
    description=(
        "Review the code for bugs and missed edge cases. Fix them and return the "
        "FINAL improved code, then one line on what you changed."
    ),
    expected_output="The final Python code block, followed by 'Changes:' and one short line.",
)

# ---------------------------------------------------------------------------
# The Crew: the specialists do the work, the Lion runs the show.
# Process.hierarchical is what makes the manager delegate the tasks.
# ---------------------------------------------------------------------------

crew = Crew(
    agents=[architect, engineer, reviewer], # the specialists - NOT the manager
    tasks=[design_task, build_task, review_task], 
    process=Process.hierarchical,
    manager_agent=manager,  # the Lion runs the crew
    verbose=True,
)


if __name__=="__main__":
     feature = "a Python function is_palindrome(text) that ignores case, spaces, and punctuation"
     result = crew.kickoff(inputs={"feature": feature})
     print("\n\n===== FINAL =====\n")
     print(result)