import os 
from dotenv import load_dotenv
load_dotenv()
from langchain_core.prompts import PromptTemplate 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent, 
    AgentExecutor, 
)
#React is the most popular way to implement the agent with the llm. 
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain import hub
from tools.tools import get_profile_url_tavily

def lookup(name : str) -> str : 
    llm = ChatGoogleGenerativeAI(model="gemini-pro",
                             temperature=0.3)
    
    template = """Given the full name {name_of_person} I want you to get it me a link to their Linkedin profile page. 
    Your answer should contain only a URL"""
    
    prompt_template = PromptTemplate(
        template = template, input_variables = ['name_of_person']
    )
    
    tools_for_agent = [
        Tool(
            name = 'Crawl Google 4 Linkedin profile page', 
            func = get_profile_url_tavily,
            description = 'useful for when you need to get the Linkedin Page URL',
        )
    ]
    react_prompt = hub.pull('hwchase17/react')
    agent = create_react_agent(llm = llm , tools = tools_for_agent, prompt = react_prompt)
    agent_executor = AgentExecutor(agent = agent, tools = tools_for_agent, verbose = True)

    result = agent_executor.invoke(
        input = {"input" : prompt_template.format_prompt(name_of_person = name)}
    )
    
    linkedin_profile_url = result['output']
    return linkedin_profile_url



if __name__ =='__main__' : 
    linkedin_url = lookup(name = 'Hitesh Ankodia')
    print(linkedin_url)