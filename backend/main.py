from flask import Flask,request
from flask_cors import CORS

 
app=Flask(__name__)
CORS(app)
 
@app.route('/')
def index():
    return 'Hello Flask!!!'
 
@app.route('/api/axios')
def msg():
    return '需要传递给前端的数据'
 
@app.route('/api/msg',methods={'POST'})
def message():
    if request.data:
        res=request.data
        print(res)
        # 这里传过来的是bytes类型数据，所以简单处理了一下，但这里主要说明数据是成功传输了过来
        res1=res.decode('utf-8')
        print(res1)
        return '获取数据成功'
    else:
        return '没有数据'
 
if __name__=="__main__":
    app.run(debug=True)
    # debug==True是为了方便修改代码之后，能够不重启项目就能够更新，否则，每次更改代码都需要重新启动项目
    # 其他参数的设置可以查阅文档，这里越简单越好