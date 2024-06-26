import re
from langchain.tools import StructuredTool
from langchain_core.output_parsers import BaseOutputParser, StrOutputParser
from langchain_core.prompts import PromptTemplate
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
from utils.CallbackHandlers import ColoredPrintHandler
from utils.PrintUtils import CODE_COLOR
from langchain_openai import ChatOpenAI
from openai import OpenAI
from ExcelTool import get_first_n_rows, get_column_names
from langchain_experimental.utilities import PythonREPL


from langchain_community.chat_models import QianfanChatEndpoint
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

class PythonCodeParser(BaseOutputParser):
    """从OpenAI返回的文本中提取Python代码。"""

    @staticmethod
    def __remove_marked_lines(input_str: str) -> str:
        lines = input_str.strip().split('\n')
        if lines and lines[0].strip().startswith('```'):
            del lines[0]
        if lines and lines[-1].strip().startswith('```'):
            del lines[-1]

        ans = '\n'.join(lines)
        return ans

    def parse(self, text: str) -> str:
        # 使用正则表达式找到所有的Python代码块
        python_code_blocks = re.findall(r'```python\n(.*?)\n```', text, re.DOTALL)
        # 从re返回结果提取出Python代码文本
        python_code = None
        if len(python_code_blocks) > 0:
            python_code = python_code_blocks[0]
            python_code = self.__remove_marked_lines(python_code)
        return python_code

# 获取当前文件的完整路径


class ExcelAnalyser:
    """
    通过程序脚本分析一个结构化文件（例如excel文件）的内容。
    输人中必须包含文件的完整路径和具体分析方式和分析依据，阈值常量等。
    """

    def __init__(self, prompt_file= "/prompts/tools/excel_analyser.txt", verbose=False):
        current_path = os.path.abspath(__file__)
        # 获取当前路径的父路径
        parent_path = os.path.dirname(current_path)
        getParentPath =  os.path.dirname(parent_path)
        # 文件读取
        content = open(getParentPath + prompt_file, "r", encoding="utf-8").read()
        self.prompt = PromptTemplate.from_template(content)
        self.verbose = verbose
        self.verbose_handler = ColoredPrintHandler(CODE_COLOR)

    def analyse(self, query, filename):

        """分析一个结构化文件（例如excel文件）的内容。"""

        # columns = get_column_names(filename)
        inspections = get_first_n_rows(filename, 3)
        # client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"),base_url=os.getenv("base_url"))
        # llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"),base_url=os.getenv("base_url"))
        # llm = ChatOpenAI(
        #     #model="gpt-4-1106-preview",
        #     api_key=os.getenv("OPENAI_API_KEY"),
        #     base_url=os.getenv("base_url")
        # )

        llm = QianfanChatEndpoint(
            qianfan_ak=os.getenv('ERNIE_CLIENT_ID'),
            qianfan_sk=os.getenv('ERNIE_CLIENT_SECRET')
        )

        code_parser = PythonCodeParser()
        chain = self.prompt | llm | StrOutputParser()

        response = ""

        for c in chain.stream({
            "query": query,
            "filename": filename,
            "inspections": inspections
        }, config={
            "callbacks": [
                self.verbose_handler
            ] if self.verbose else []
        }):
            response += c

        code = code_parser.parse(response)

        if code:
            ans = query+"\n"+PythonREPL().run(code)
            return ans
        else:
            return "没有找到可执行的Python代码"

    def as_tool(self):
        return StructuredTool.from_function(
            func=self.analyse,
            name="AnalyseExcel",
            description=self.__class__.__doc__.replace("\n", ""),
        )


if __name__ == "__main__":
    current_path = os.path.abspath(__file__)
    # 获取当前路径的父路径
    parent_path = os.path.dirname(current_path)
    getParentPath =  os.path.dirname(parent_path)
    # 文件读取
    print(ExcelAnalyser().analyse(
        query="8月销售额",
        filename=getParentPath + "/data/2023年8月-9月销售记录.xlsx"
    ))
