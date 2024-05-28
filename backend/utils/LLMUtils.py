from langchain.schema import BaseOutputParser
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import QianfanChatEndpoint
from langchain_core.messages import HumanMessage
import os
from dotenv import load_dotenv, find_dotenv
from langchain_core.prompts import PromptTemplate
import sys
from langchain.schema import BaseOutputParser
import re
import numpy as np
from tqdm import tqdm
from collections import defaultdict
from typing import List, Dict, Any, Tuple
from transformers import RagTokenizer, RagRetriever, RagSequenceForGeneration, RagTokenForGeneration
from transformers import BertTokenizer, BertForQuestionAnswering, BertConfig
from transformers import pipeline
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv
import json
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
import nltk
import re
import warnings
warnings.simplefilter("ignore")  # 屏蔽 ES 的一些Warnings

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
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"),base_url=os.getenv("base_url"))
def to_keywords(input_string):
    '''（英文）文本只保留关键字'''
    # 使用正则表达式替换所有非字母数字的字符为空格
    no_symbols = re.sub(r'[^a-zA-Z0-9\s]', ' ', input_string)
    word_tokens = word_tokenize(no_symbols)
    # 加载停用词表
    stop_words = set(stopwords.words('english'))
    ps = PorterStemmer()
    # 去停用词，取词根
    filtered_sentence = [ps.stem(w) for w in word_tokens if not w.lower() in stop_words]
    getstr = ' '.join(filtered_sentence)
    print(getstr)
    return getstr
# 创建elastic search连接
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
# 列出所有es 中的index
# Get a list of all indices in the cluster
indices = es.cat.indices(format='json')
# 查询所有索引
all_indices = es.indices.get_alias("*").keys()
# 替换成你的索引名称和查询条件
index_name = list(all_indices)[0]
print(index_name)
query_body = {
    "query": {
        "match_all": {}
    }
}

index_name = 'van34691_scheduleeyecaremodeandaccesstolocation'
def search(query_string, top_n=3):
    # ES 的查询语言
    search_query = {
        "match": {
            "keywords": to_keywords(query_string)
        }
    }
    print(search_query)
    body = {
        "query": {
            "match_all": {}
        }
    }
    res = es.search(index=index_name, body=body, size=top_n)
    if res == None:
        print('no result')
        return []
    print(res)
    return [hit["_source"]["content"] for hit in res["hits"]["hits"]]
# 从ES中检索数据
def get_completion(prompt, model="gpt-3.5-turbo-1106"):
    '''封装 openai 接口'''
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,  # 模型输出的随机性，0 表示随机性最小
    )
    return response.choices[0].message.content

def build_prompt(prompt_template, **kwargs):
    '''将 Prompt 模板赋值'''
    inputs = {}
    for k, v in kwargs.items():
        if isinstance(v, list) and all(isinstance(elem, str) for elem in v):
            val = '\n\n'.join(v)
        else:
            val = v
        inputs[k] = val
    return prompt_template.format(**inputs)

prompt_template = """
你是为CSW自动化测试定制AI1.0版本的机器人，不仅支持多轮对话，还能回答关于项目的问题。
你的任务是回答用户问题
用户问：
{query}
"""

def GetOut(task):
    #chain = prompt | model | output_parser
    #user_query = "有多少个 VAN34691_TestStep"
    user_query = task 
    # 1. 检索
    search_results = search(user_query, 2)
    # 2. 构建 Prompt
    prompt = build_prompt(prompt_template, context=search_results, query=user_query)
    print("===Prompt===")
    print(prompt)
    # 3. 调用 LLM
    response = get_completion(prompt)
    print("===回复===")
    print(response)
    return str(response)

# # Path: backend/utils/LLMUtils.py
# # Compare this snippet from backend/main.py:
# GetOut("你是谁")