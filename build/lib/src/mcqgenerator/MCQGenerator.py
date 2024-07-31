import os, json, pandas as pd

from src.mcqgenerator.utils import read_file, get_table_data 
from src.mcqgenerator.logger import logging 

# import necessary packages from langchain 
# from langchain.llms import OpenAI  (deprecated )
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate 
from langchain.chains import LLMChain 
from langchain.chains import SequentialChain 


#from langchain.chat_models import ChatOpenAI
# LangChainDeprecationWarning: The class `langchain_community.chat_models.openai.ChatOpenAI` was deprecated in langchain-community 0.0.10 and will be removed in 0.2.0. 
# An updated version of the class exists in the langchain-openai package and should be used instead. To use it run `pip install -U langchain-openai` and import as `from langchain_openai import ChatOpenAI`.
from langchain_openai import ChatOpenAI


from dotenv import load_dotenv
load_dotenv() # taking env variables from .env file. 
mykey=os.environ["OPENAI_API_KEY"]
models=["gpt-3.5", "gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"]  #  model choices 

# temperature   0 - more determinisic.   2 - more randomness 
llm=ChatOpenAI(openai_api_key=mykey, model_name="gpt-3.5-turbo", temperature=0.5)


template="""
You are an expert MCQ maker and an expert in the subject {subject}. It is your job to \
create a quiz  of {number} multiple choice questions for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}

"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["number", "subject", "tone", "response_json"],
    template=template 
    )

quiz_chain = LLMChain(llm=llm, prompts=quiz_generation_prompt, output_key = "quiz", verbose = True)

template2="""
You are an expert english grammarian and writer and an expert in the subject {subject} . Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at par with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student's abilities
Quiz_MCQs:
{quiz}


Check from an expert English Writer of the above quiz:
"""

quiz_evaluation_prompt = PromptTemplate(input_varibles = ["subject", "quiz"], template = template2 )

review_chain = LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key = "review", verbose = True)

# this is an overall chain where we run the two chains in sequence 
generate_evaluate_chain=SequentialChain(chains=[quiz_chain, review_chain], input_variables=["number", "subject", "tone", "response_json"],
                                        output_variables=["quiz", "review"], verbose=True)


