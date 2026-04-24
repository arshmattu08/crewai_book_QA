# imports
import agentops
import os
from crewai import Agent, Task, Crew
from crewai_tools import FileReadTool, PDFSearchTool, DOCXSearchTool
from dotenv import load_dotenv

# basic setup
load_dotenv()
agentops.init()
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o-mini'
# Create the tool with a SPECIFIC, VISIBLE path for the database
pdf_search_tool = PDFSearchTool(pdf="assets/ISLR.pdf")
    

# if file saving required
# OUTPUT_DIR = 'crew_outputs'
# os.makedirs(OUTPUT_DIR, exist_ok=True)


# Agent definitions
## Searcher/answerer
search_agent = Agent(
    role = "search the given document based on user query and answer the query",
    goal = "after having searched the given document, provide accurate answers",
    tools = [pdf_search_tool],
    backstory = "You're a document searcher which provides accurate answers based on a given query by user"
)

# Task definitions
search_task = Task(
    description=("Given a user query {user_query}, search through the provided document and provide accurate and relevant answer to user"
    ),
    expected_output="Provided answer to {user_query} based on what you found.",
    agent= search_agent
)

# Crew setup and kickoff
rag_crew = Crew(
    agents= [search_agent],
    tasks= [search_task],
    verbose= True
)

query = {"user_query":"What is Logistic Regression?"}
rag_crew.kickoff(inputs= query)