from ast import mod

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import scrap_web, web_search
import os
from dotenv import load_dotenv

load_dotenv()
#model setup
model = ChatOpenAI(model='gpt-4o-mini',temperature=0)

# First agent

def build_search_agent():
    return create_agent(
        model=model,
        tools=[web_search]
    )


# Second Agent
def builder_reader_agent():
    return create_agent(
        model=model,
        tools=[scrap_web]
    )

#writer chain(Runnables)


write_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

writer_chain = write_prompt | model | StrOutputParser()

#critic_chain

critic_promt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_promt | model | StrOutputParser()


