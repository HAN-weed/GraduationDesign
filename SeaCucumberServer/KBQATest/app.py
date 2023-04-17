from flask import Flask, jsonify, request, Response, json
import os
import sys

from chat_graph import ChatGraph
from graph2json import Graph2json
from keyword_extraction import KeywordExtraction

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

'''图片访问接口'''
@app.route("/photo/<urlId>")
def get_frame(urlId):
    with open(r'img/{}.png'.format(urlId),'rb') as f:
        image = f.read()
        resp = Response(image,mimetype="image/jpg")
        return resp
'''提问接口'''
@app.route('/question/<question>',methods = ['GET'])
def kbqa(question):
    bot  = ChatGraph()
    tmp_res,img_res = bot.chat(question)
    res_map = {
        'text_answer': tmp_res,
        'img_answer': img_res
    }
    res = text_response(res_map,True,[])
    return res

'''关键词抽取接口'''
@app.route('/keyword/<question>',methods = ['GET'])
def getKeyword(question):
    keyword_extraction  = KeywordExtraction()
    tmp_res = keyword_extraction.keyword_extraction_main(question)
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
