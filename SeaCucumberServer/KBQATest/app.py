from flask import Flask, jsonify, request
import os
import sys

from chat_graph import ChatGraph
from graph2json import Graph2json

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

question_instance = {}


@app.route('/hello')
def hello_world():
    return 'Hello World!'

def text_response(text,success,nodes=[]):
    tmp = {
        'text' : text,
        'nodes' : nodes,
        'success' : success
    }
    return jsonify(tmp)

'''提问接口'''
@app.route('/question/<question>',methods = ['GET'])
def kbqa(question):
    bot  = ChatGraph()
    tmp_res = bot.chat(question)
    nodes = []
    entity = ""
    ans = ""
    res = text_response(tmp_res,True,[])
    print(res)
    return res

'''知识图谱json数据接口'''
@app.route('/knowledgeGraph/allData',methods = ['GET'])
def allData():
    match = Graph2json()
    response = text_response(match.graph2json_main(),True,[])
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8000)
