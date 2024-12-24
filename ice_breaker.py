from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from output_parsers import summary_parser, Summary
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from typing import Tuple

def ice_break_with(name: str) -> Tuple[Summary, str] : 
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url=linkedin_username, mock=True
    )

    
    print("Before Summary Template")
    summary_template = """
    given the Linkedin information {information} about a person I want you to create:
    1. A short summary
    2. two interesting facts about them
    

    Use  information from  Linkedin
    \n{format_instructions}
    """
    summary_prompt_template = PromptTemplate(
        input_variables=["information", ],
        template=summary_template,
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions()
        },
    )

        
    llm = ChatGoogleGenerativeAI(model="gemini-pro",
                             temperature=0)
    chain = summary_prompt_template | llm | summary_parser

    res : Summary = chain.invoke(input={"information": linkedin_data})
    print("Before return")
    print(res)
    print(linkedin_data.get("profile_pic_url"))
    return res, linkedin_data.get("profile_pic_url")
    

if __name__ == "__main__":
    load_dotenv()

    print("Ice Breaker Enter")
    summary, profile_pic_url = ice_break_with(name="Eden Marco")