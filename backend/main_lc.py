from typing import Union
from langchain.output_parsers import OutputFixingParser
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from pydantic import BaseModel, Field
from langchain.agents import AgentExecutor, create_react_agent, AgentOutputParser
from langchain_openai import ChatOpenAI
from Tools import *
from Tools.PythonTool import ExcelAnalyser
import os
import sys

from dotenv import load_dotenv, find_dotenv
# Python  引入其他文件夹里的文件
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
from utils.CallbackHandlers import ColoredPrintHandler
from utils.PrintUtils import THOUGHT_COLOR

# 加载环境变量
_ = load_dotenv(find_dotenv())


class MyAgentOutputParser(AgentOutputParser):
    """自定义parser，从思维链中取出最后的Y/N"""
    class AgentActionWrapper(BaseModel):
        tool: str = Field(..., title="The name of the Tool to execute.")
        tool_input: Union[str, dict] = Field(..., title="The input to pass in to the Tool.")

    __action_parser = OutputFixingParser.from_llm(
        parser=PydanticOutputParser(pydantic_object=AgentActionWrapper),
        llm=ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            model_kwargs={"seed": 42}
        )
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def parse(self, text: str) -> Union[AgentAction, AgentFinish]:
        action = self.__action_parser.parse(text)
        if action.tool == "FINISH":
            return AgentFinish(log=text, return_values={
                "output": list(action.tool_input.values())[0]
                if isinstance(action.tool_input, dict)
                else action.tool_input
            })

        return AgentAction(
            tool=action.tool,
            tool_input=action.tool_input,
            log=text
        )

    def get_format_instructions(self) -> str:
        return self.__action_parser.get_format_instructions()


def run_agent(agent, tools):
    human_icon = "\U0001F468"
    ai_icon = "\U0001F916"

    message_history = ChatMessageHistory()

    callback_handlers = [
        ColoredPrintHandler(color=THOUGHT_COLOR)
    ]

    while True:
        task = input(f"{ai_icon}：有什么可以帮您？\n{human_icon}：")
        if task.strip().lower() == "quit":
            break
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            handle_parsing_errors=True
        )

        agent_with_chat_history = RunnableWithMessageHistory(
            agent_executor,
            # This is needed because in most real world scenarios, a session id is needed
            # It isn't really used here because we are using a simple in memory ChatMessageHistory
            lambda session_id: message_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )

        # 执行
        reply = ""
        for s in agent_with_chat_history.stream(
                {"input": task},
                config={
                    "configurable": {"session_id": "<foo>"},
                    "callbacks": callback_handlers
                },
        ):
            if "output" in s:
                reply = s["output"]

        print(f"{ai_icon}：{reply}\n")


def main():
    # 语言模型
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        model_kwargs={
            "seed": 42
        }
    )

    # 自定义工具集
    tools = [
        document_qa_tool,
        document_generation_tool,
        email_tool,
        excel_inspection_tool,
        directory_inspection_tool,
        finish_placeholder,
        ExcelAnalyser(
            prompt_file="./prompts/tools/excel_analyser.txt",
            verbose=True
        ).as_tool()
    ]

    parser = MyAgentOutputParser()
    current_path = os.path.abspath(__file__)
        # 获取当前路径的父路径
    parent_path = os.path.dirname(current_path)
    #getParentPath =  os.path.dirname(parent_path)
        # 文件读取
    content = open(parent_path + '/prompts/main/main.txt', "r", encoding="utf-8").read()
    prompt = PromptTemplate.from_template(content)
    prompt = prompt.partial(
        work_dir= "./data",
        format_instructions=parser.get_format_instructions()
    )

    # 定义智能体
    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt,
        output_parser=parser
    )

    # 启动智能体
    run_agent(agent, tools)


if __name__ == "__main__":
    main()
