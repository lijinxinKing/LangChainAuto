from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import BaseOutputParser
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import QianfanChatEndpoint
from langchain_core.messages import HumanMessage
import os
from dotenv import load_dotenv, find_dotenv
from langchain_core.prompts import PromptTemplate
import sys
#获取当前路径的上一级路径
from langchain.schema import BaseOutputParser
import os
 
# 获取当前文件的完整路径
current_path = os.path.abspath(__file__)
# 获取当前路径的父路径
parent_path = os.path.dirname(current_path)
getParentPath =  os.path.dirname(parent_path)

_ = load_dotenv(find_dotenv())

llm = QianfanChatEndpoint(
    qianfan_ak=os.getenv('ERNIE_CLIENT_ID'),
    qianfan_sk=os.getenv('ERNIE_CLIENT_SECRET')
)

class CommaSeparatedListOutputParser(BaseOutputParser):
    """Parse the output of an LLM call to a comma-separated list."""
    def parse(self, text: str):
        """Parse the output of an LLM call."""
        return text.strip().split(", ")

model = llm
output_parser = CommaSeparatedListOutputParser()
# 它将不同的组件链接在一起，将一个组件的输出作为下一个组件的输入

promptFile = getParentPath + "\\prompts\\main\\main.txt"
print(promptFile)
promptContent = open(promptFile, 'r', encoding='utf-8').read()
prompt = PromptTemplate.from_template(promptContent)
# 自定义工具集

template = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            "{product}不仅支持多轮对话，自动回答问题，还能回答关于项目的问题。你的名字叫{name}"),
        HumanMessagePromptTemplate.from_template("{query}"),
    ]
)

prompt = template.format_messages(
    product="为CSW自动化测试定制AI1.0版本",
    name="AiAuto",
    query="你是谁"
)

def GetOut(task):
    #chain = prompt | model | output_parser
    ouot = llm.invoke(prompt)
    print(ouot)
    return ouot

# Path: backend/utils/LLMUtils.py
# Compare this snippet from backend/main.py:
GetOut("你是谁")