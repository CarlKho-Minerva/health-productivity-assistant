import os
import logging
import wikipedia
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.agents import SequentialAgent
from google.adk.tools.tool_context import ToolContext

load_dotenv()
logging.basicConfig(level=logging.INFO)

model_name = os.getenv("MODEL", "gemini-3-flash-preview")


def add_prompt_to_state(tool_context: ToolContext, prompt: str) -> dict:
    """Saves the user's initial prompt to the state."""
    tool_context.state["user_prompt"] = prompt
    return {"status": "success"}


def search_wikipedia(query: str) -> str:
    """Search Wikipedia for information about an animal or topic."""
    try:
        return wikipedia.summary(query, sentences=8, auto_suggest=False)
    except wikipedia.exceptions.DisambiguationError as e:
        return wikipedia.summary(e.options[0], sentences=8)
    except Exception as e:
        return f"Could not find Wikipedia info: {str(e)}"


# Greet user and save their prompt

def add_prompt_to_state(
    tool_context: ToolContext, prompt: str
) -> dict:
    """Saves the user's initial prompt to the state."""
    tool_context.state["user_prompt"] = prompt
    logging.info(f"Prompt saved to state: {prompt}")
    return {"status": "success"}


# Configuring the Wikipedia Tool
wikipedia_tool = search_wikipedia


# 1. Researcher Agent
comprehensive_researcher = Agent(
    name="comprehensive_researcher",
    model=model_name,
    description="Researches animal information from Wikipedia on behalf of zoo visitors.",
    instruction="""You are a comprehensive animal researcher for a zoo tour.
    The visitor's question has been saved in state['user_prompt'].
    Your job is to:
    1. Read the visitor's question from state['user_prompt']
    2. Use the wikipedia tool to look up relevant information about the animal or topic
    3. Gather comprehensive facts including diet, habitat, behavior, lifespan, and fun facts
    Be thorough — collect as much relevant information as possible.
    """,
    tools=[search_wikipedia],
    output_key="research_data"  # A key to store the combined findings
)


# 2. Response Formatter Agent
response_formatter = Agent(
    name="response_formatter",
    model=model_name,
    description="Formats research data into a friendly zoo tour guide response.",
    instruction="""You are a friendly and enthusiastic Zoo Tour Guide.
    The visitor's original question is in state['user_prompt'].
    The research findings gathered for them are in state['research_data'].

    Transform the research into a warm, engaging, and informative response.
    Be conversational and friendly — suitable for zoo visitors of all ages.
    Highlight interesting facts, and make the experience feel personal and exciting.
    """
)


tour_guide_workflow = SequentialAgent(
    name="tour_guide_workflow",
    description="Orchestrates research and response formatting for zoo visitor questions.",
    sub_agents=[
        comprehensive_researcher,
        response_formatter,
    ]
)


root_agent = Agent(
    name="greeter",
    model=model_name,
    description="The main Zoo Tour Guide greeter that welcomes visitors and answers their animal questions.",
    instruction="""You are a friendly Zoo Tour Guide greeter.
    Warmly welcome the visitor to the zoo.
    Ask them what animal they would like to learn about or what they need help with today.
    When the visitor provides their question or request, use the add_prompt_to_state tool
    to save their exact words, passing them as the 'prompt' argument.
    After the tool confirms success, hand off to the tour_guide_workflow to research and answer.
    """,
    tools=[add_prompt_to_state],
    sub_agents=[tour_guide_workflow]
)
