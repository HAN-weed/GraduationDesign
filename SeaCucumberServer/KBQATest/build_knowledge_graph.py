## 相关模块导入
import pandas as pd
from py2neo import Graph,Node,Relationship

class BuildKnowledgeGraph:
    def __init__(self):
        ## 连接图形库，配置neo4j
        self.graph = Graph("bolt://localhost:7687", auth=('neo4j', '123456'))
        # 清空全部数据
        self.graph.delete_all()
        # 开启一个新的事务
        self.graph.begin()

    '''数据导入及知识图谱构建'''
    def build_knowledge_graph_main(self):
        ## csv源数据读取
        diseaseData = pd.read_csv('./data/disease.csv', encoding='utf-8')
        has_symptomData = pd.read_csv('./data/has_symptom.csv', encoding='utf-8')
        # 获取所有列标签
        columnLst_disease = diseaseData.columns.tolist()
        columnLst_has_symptom = has_symptomData.columns.tolist()
        print(columnLst_disease)
        print(columnLst_has_symptom)

        '''将Disease数据导入neo4j'''
        # 获取数据数量
        num = len(diseaseData['name'])
        for i in range(num):
            dict = {}
            # 为每个疾病实体构建属性字典
            for column in columnLst_disease:
                dict[column] = diseaseData[column][i]
            # 根据数据内容拼接cypher
            cypher = "MERGE (n: Disease {name:'%s',introduction:'%s',cause:'%s',pathogen:'%s',characteristic:'%s',easy_get:'%s',prevent:'%s',cure:'%s'})" \
                     % (diseaseData['name'][i], diseaseData['introduction'][i], diseaseData['cause'][i],
                        diseaseData['pathogen'][i], diseaseData['characteristic'][i], diseaseData['easy_get'][i],
                        diseaseData['prevent'][i], diseaseData['cure'][i])
            self.graph.run(cypher)

        '''将has_symptom关系数据导入neo4j'''
        # 获取数据数量
        num = len(has_symptomData['disease'])
        for i in range(num):
            dict = {}
            # 为每个疾病-症状关系构建属性字典
            for column in columnLst_has_symptom:
                dict[column] = has_symptomData[column][i]
            # 根据数据内容拼接cypher
            cypher_createSymptom = "MERGE (n:Symptom {name:'%s'})"% has_symptomData['symptom'][i]
            cypher = "MATCH (n: Disease {name : '%s'}) , (m: Symptom {name : '%s'})  with n,m CREATE (n)-[:has_symptom]->(m)"%(has_symptomData['disease'][i],has_symptomData['symptom'][i])

            print(cypher_createSymptom)
            print(cypher)
            self.graph.run(cypher_createSymptom)
            self.graph.run(cypher)



if __name__ == '__main__':
    handler = BuildKnowledgeGraph()
    handler.build_knowledge_graph_main()
