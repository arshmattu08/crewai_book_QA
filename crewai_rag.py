# imports
import agentops
import os
from crewai import Agent, Task, Crew
from crewai_tools import FileReadTool, PDFSearchTool
from dotenv import load_dotenv

# basic setup
load_dotenv()
agentops.init()
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o-mini'

# Agent definitions

## Searcher/answerer
search_agent = Agent(
    role = "search the given document",
    goal = "after having searched the given document, provide accurate answers",
    tools = FileReadTool(file_path="assets/learning_spark.pdf"),
    backstory = "You're a document searcher which provides accurate answers based on a given query by user"
)

## grader/evaluator
evaluator_agent = Agent(
    role = "Check the answers of previous search agent",
    goal = "Check answers of previous agent and make sure you search again so that the provided answer is accurate",
    tools = "",
    backstory = "You're an evaluator who double checks the information and makes sure it is accurate"
)

# Task definitions
search_task = Task(
    description=("Search through the provided document and provide accurate and relevant answer to user"
    "If correct answer not found then say answer not found"),
    expected_output="A text answer which is accurate and relevant to the user query if not found say answer not found",
    agent= search_agent
)

eval_task = Task(
    description= ("Double check the previous agent's work"
                  ),
    expected_output= "Answer received from previous agent or say answer not found if answer actually not found",
    agent = evaluator_agent
)

# Crew setup and kickoff