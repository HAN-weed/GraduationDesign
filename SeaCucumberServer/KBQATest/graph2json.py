## 相关模块导入
import json

import pandas as pd
from py2neo import Graph, Node, Relationship


class Graph2json:
    def __init__(self):
        ## 连接图形库，配置neo4j
        self.graph = Graph("bolt://localhost:7687", auth=('neo4j', '123456'))
        # 开启一个新的事务
        self.graph.begin()

    def graph2json_main(self):
        # 定义data数组，存放节点信息
        data = []
        # 定义关系数组，存放节点间的关系
        links = []
        # 查询所有节点，并将节点信息取出存放在data数组中
        for n in self.graph.nodes.match("Disease"):
            node_name = n['name']
            # 构造字典，存储单个节点信息
            dict = {
                'name': node_name,
                'category': 'Disease'
            }
            # 将单个节点信息存放在data数组中
            data.append(dict)
        for n in self.graph.nodes.match("Symptom"):
            node_name = n['name']
            # 构造字典，存储单个节点信息
            dict = {
                'name': node_name,
                'category': 'Symptom'
            }
            # 将单个节点信息存放在data数组中
            data.append(dict)
        for n in self.graph.nodes.match("Alias"):
            node_name = n['name']
            # 构造字典，存储单个节点信息
            dict = {
                'name': node_name,
                'category': 'Alias'
            }
            # 将单个节点信息存放在data数组中
            data.append(dict)
        for n in self.graph.nodes.match("Disease_Kind"):
            node_name = n['name']
            # 构造字典，存储单个节点信息
            dict = {
                'name': node_name,
                'category': 'Disease_Kind'
            }
            # 将单个节点信息存放在data数组中
            data.append(dict)
        for n in self.graph.nodes.match("Drug"):
            node_name = n['name']
            # 构造字典，存储单个节点信息
            dict = {
                'name': node_name,
                'category': 'Drug'
            }
            # 将单个节点信息存放在data数组中
            data.append(dict)
        for n in self.graph.nodes.match("Pathogen"):
            node_name = n['name']
            # 构造字典，存储单个节点信息
            dict = {
                'name': node_name,
                'category': 'Pathogen'
            }
            # 将单个节点信息存放在data数组中
            data.append(dict)
        rps = self.graph.relationships
        for r in rps:
            # 取出开始节点的name
            source = str(rps[r].start_node['name'])
            # 取出结束节点的name
            target = str(rps[r].end_node['name'])
            # 取出开始节点的结束节点之间的关系
            name = str(type(rps[r]).__name__)
            # 构造字典存储单个关系信息
            dict = {
                'source': source,
                'target': target,
                'name': name
            }
            # 将单个关系信息存放进links数组中
            links.append(dict)
        # 输出所有节点信息
        for item in data:
            print(item)
        # 输出所有关系信息
        for item in links:
            print(item)
        # 将所有的节点信息和关系信息存放在一个字典中
        neo4j_data = {
            'data': data,
            'links': links
        }
        print(neo4j_data)
        # 将字典转化json格式
        # neo4j_data = json.dumps(neo4j_data)
        # with open(r"C:\Users\asus\Desktop\毕设\Project\SeaCucumberServer\KBQATest\js\neoData.json", "w", encoding='utf-8') as f:
        #     # jsontext是neo4j返回的数据
        #     js = json.dumps(neo4j_data)
        #     f.write(js)
        return neo4j_data


if __name__ == '__main__':
    handler = Graph2json()
    print(handler.graph2json_main())
