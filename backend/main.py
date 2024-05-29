from flask import Flask,request
from flask_cors import CORS
from utils import LLMUtils
import json 
from langchain_core.prompts import PromptTemplate

app=Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'Hello AI Auto Agent !!!'

@app.route('/ask',methods=['POST'])
def post():
    if request.form:
        res = request.form
        print(res)
        getAllKeys = list(res.keys())
        print(getAllKeys[0])
        text = json.loads(getAllKeys[0])
        print(len(text))
        textLene = len(text) - 1
        content = text[textLene].get('content')
        role = text[textLene].get('role')
        print(content)
        print(role)
        oout = LLMUtils.GetOut(content)
        return str(oout)
    else:
        return '没有数据'
 
if __name__=="__main__":
    app.run(debug=True,host="10.119.150.151", port=5000)
    # debug==True是为了方便修改代码之后，能够不重启项目就能够更新，否则，每次更改代码都需要重新启动项目
    # 其他参数的设置可以查阅文档，这里越简单越好