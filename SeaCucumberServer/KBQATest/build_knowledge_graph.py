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
        imgData = pd.read_csv('./data/img.csv', encoding='utf-8')
        # symptomData = pd.read_csv('./data/symptom.csv', encoding='utf-8')
        has_symptomData = pd.read_csv('./data/has_symptom.csv', encoding='utf-8')
        belongs_toData = pd.read_csv('./data/belongs_to.csv', encoding='utf-8')
        alias_isData = pd.read_csv('./data/alias_is.csv', encoding='utf-8')
        cause_byData = pd.read_csv('./data/cause_by.csv', encoding='utf-8')
        recommend_drugData = pd.read_csv('./data/recommend_drug.csv', encoding='utf-8')
        related_imgData = pd.read_csv('./data/related_img.csv', encoding='utf-8')

        '''将Disease数据导入neo4j'''
        # 获取数据数量
        num = len(diseaseData['name'])
        for i in range(num):
            # 根据数据内容拼接cypher
            cypher = "MERGE (n: Disease {name:'%s',introduction:'%s',cause:'%s',easy_get:'%s',prevent:'%s',cure:'%s'})" \
                     % (diseaseData['name'][i], diseaseData['introduction'][i], diseaseData['cause'][i],
                        diseaseData['easy_get'][i],diseaseData['prevent'][i], diseaseData['cure'][i])
            print(cypher)
            self.graph.run(cypher)

        # '''将Symptom数据导入neo4j'''
        # # 获取数据数量
        # num = len(symptomData['name'])
        # for i in range(num):
        #     # 根据数据内容拼接cypher
        #     cypher = "MERGE (n: Symptom {name:'%s',detail:'%s'})" \
        #              % (symptomData['name'][i], symptomData['detail'][i])
        #     print(cypher)
        #     self.graph.run(cypher)

        '''将has_symptom关系数据导入neo4j'''
        # 获取数据数量
        num = len(has_symptomData['disease'])
        for i in range(num):
            # 根据数据内容拼接cypher
            createcypher = "MERGE (n: Symptom {name:'%s'})" % has_symptomData['symptom'][i]
            cypher = "MATCH (n: Disease {name : '%s'}) , (m: Symptom {name : '%s'})  with n,m CREATE (n)-[:has_symptom]->(m)"%(has_symptomData['disease'][i],has_symptomData['symptom'][i])
            print(createcypher)
            print(cypher)
            self.graph.run(createcypher)
            self.graph.run(cypher)

        '''将belongs_to关系数据导入neo4j'''
        # 获取数据数量
        num = len(belongs_toData['disease'])
        for i in range(num):
            # 根据数据内容拼接cypher
            createcypher = "MERGE (n: Disease_Kind {name:'%s'})"%belongs_toData['disease_kind'][i]
            cypher = "MATCH (n: Disease {name : '%s'}) , (m: Disease_Kind {name : '%s'})  with n,m CREATE (n)-[:belongs_to]->(m)" % (
            belongs_toData['disease'][i], belongs_toData['disease_kind'][i])
            reversecypher = "MATCH (n: Disease_Kind {name : '%s'}) , (m: Disease {name : '%s'})  with n,m CREATE (n)-[:contains]->(m)" % (
            belongs_toData['disease_kind'][i], belongs_toData['disease'][i])
            print(createcypher)
            print(cypher)
            self.graph.run(createcypher)
            self.graph.run(cypher)
            self.graph.run(reversecypher)

        '''将alias_is关系数据导入neo4j'''
        # 获取数据数量
        num = len(alias_isData['disease'])
        for i in range(num):
            # 根据数据内容拼接cypher
            createcypher = "MERGE (n: Alias {name:'%s'})" % alias_isData['alias'][i]
            cypher = "MATCH (n: Disease {name : '%s'}) , (m: Alias {name : '%s'})  with n,m CREATE (n)-[:alias_is]->(m)" % (
                alias_isData['disease'][i], alias_isData['alias'][i])
            print(createcypher)
            print(cypher)
            self.graph.run(createcypher)
            self.graph.run(cypher)

        '''将cause_by关系数据导入neo4j'''
        # 获取数据数量
        num = len(cause_byData['disease'])
        for i in range(num):
            # 根据数据内容拼接cypher
            createcypher = "MERGE (n: Pathogen {name:'%s'})" % cause_byData['pathogen'][i]
            cypher = "MATCH (n: Disease {name : '%s'}) , (m: Pathogen {name : '%s'})  with n,m CREATE (n)-[:cause_by]->(m)" % (
                cause_byData['disease'][i], cause_byData['pathogen'][i])
            print(createcypher)
            print(cypher)
            self.graph.run(createcypher)
            self.graph.run(cypher)


        '''将recommend_drug关系数据导入neo4j'''
        # 获取数据数量
        num = len(recommend_drugData['disease'])
        for i in range(num):
            # 根据数据内容拼接cypher
            createcypher = "MERGE (n: Drug {name:'%s'})" % recommend_drugData['drug'][i]
            cypher = "MATCH (n: Disease {name : '%s'}) , (m: Drug {name : '%s'})  with n,m CREATE (n)-[:recommend_drug]->(m)" % (
                recommend_drugData['disease'][i], recommend_drugData['drug'][i])
            reversecypher = "MATCH (n: Drug {name : '%s'}) , (m: Disease {name : '%s'})  with n,m CREATE (n)-[:to_cure]->(m)" % (
                recommend_drugData['drug'][i], recommend_drugData['disease'][i])
            print(createcypher)
            print(cypher)
            self.graph.run(createcypher)
            self.graph.run(cypher)
            self.graph.run(reversecypher)

        '''将img数据导入neo4j'''
        # 获取数据数量
        num = len(imgData['name'])
        for i in range(num):
            # 根据数据内容拼接cypher
            cypher = "MERGE (n: Img {name:'%s',detail:'%s',urlId:'%s'})" \
                     % (imgData['name'][i], imgData['detail'][i],imgData['urlId'][i])
            print(cypher)
            self.graph.run(cypher)

        '''将related_img关系数据导入neo4j'''
        # 获取数据数量
        num = len(related_imgData['disease'])
        for i in range(num):
            # 根据数据内容拼接cypher
            cypher = "MATCH (n: Disease {name : '%s'}) , (m: Img {name : '%s'})  with n,m CREATE (n)-[:related_img]->(m)" % (
            related_imgData['disease'][i], related_imgData['img'][i])
            print(cypher)
            self.graph.run(cypher)

if __name__ == '__main__':
    handler = BuildKnowledgeGraph()
    handler.build_knowledge_graph_main()
