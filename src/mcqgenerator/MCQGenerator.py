import os
import json 
import traceback
import pandas as pd 
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data 
from src.mcqgenerator.logger import logging 


# import necessary packages from langchain 
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

from langchain_openai import ChatOpenAI
from langchain.callbacks import get_openai_callback


# load env variables from the .env file. 
load_dotenv() 

mykey=os.environ["OPENAI_API_KEY"]
# temperature   0 - more determinisic.   2 - more randomness 
llm=ChatOpenAI(openai_api_key=mykey, model_name="gpt-3.5-turbo", temperature=0.7)



template="""
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz  of {number} multiple choice questions for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}

"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=template 
    )

quiz_chain = LLMChain(llm=llm, prompts=quiz_generation_prompt, output_key = "quiz", verbose = True)

template2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

quiz_evaluation_prompt = PromptTemplate(input_varibles = ["subject", "quiz"], template = template2 )

review_chain = LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key = "review", verbose = True)

# this is an overall chain where we run the two chains in sequence 
generate_evaluate_chain=SequentialChain(chains=[quiz_chain, review_chain], input_variables=["text", "number", "subject", "tone", "response_json"],
                                        output_variables=["quiz", "review"], verbose=True)


file_path=r"G:\My Drive\backup jerry-200k(master copy)\AI\project_MCQ\data_geometry.txt"

with open(file_path, 'r') as file: 
    TEXT=file.read() 
    
file_path=r"G:\My Drive\backup jerry-200k(master copy)\AI\project_MCQ\Response.json"

with open(file_path, 'r') as file: 
    RESPONSE_JSON=file.read() 


NUMBER=5
SUBJECT="Geometry" 
TONE="Difficult"

#https://python.langchain.com/docs/modules/model_io/llms/token_usage_tracking

#How to setup Token Usage Tracking in LangChain
with get_openai_callback() as cb:
    response=generate_evaluate_chain(
        {
            "text": TEXT,
            "number": NUMBER,
            "subject":SUBJECT,
            "tone": TONE,
            "response_json": json.dumps(RESPONSE_JSON)
        }
    )
    






