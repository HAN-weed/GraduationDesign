from question_classifier import *
from question_parser import *
from answer_search import *

'''关键词提取'''
class KeywordExtraction:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.g = Graph("bolt://localhost:7687", auth=('neo4j', '123456'))
        self.num_limit = 20

        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.disease_path = os.path.join(cur_dir, 'dict/disease.txt')
        self.disease_wds = [i.strip() for i in open(self.disease_path, encoding='utf-8') if i.strip()]

    def keyword_extraction_main(self,question):
        # tags = ["大型藻类","敌害动物","浒苔","化板病","化皮病","霉菌病",
        #         "寄生虫病","金膜藻","烂边病","烂胃病","强硬刚毛藻","盾纤毛虫病",
        #         "曲褶刚毛藻","软丝藻","水云"]
        '''问句分类'''
        data = {}
        dict = self.classifier.check_medical(question)
        if not dict:
            return {}
        data['args'] = dict
        types = []
        for type_ in dict.values():
            types += type_

        print(types)
        keyword_type = 'others'
        keyword_types = []
        # 1.问题中直接包含疾病信息
        if 'disease' in types:
            keyword_type = "directly_keyword"
            keyword_types.append(keyword_type)

        # 2.问题中以症状出现->疾病关键字
        elif 'symptom' in types:
            keyword_type = "symptom_keyword"
            keyword_types.append(keyword_type)

        # 2.问题中以症状出现->疾病关键字
        elif 'drug' in types:
            keyword_type = "drug_keyword"
            keyword_types.append(keyword_type)
        '''问句解析'''
        args = data['args']
        entity_dict = self.parser.build_entitydict(args)
        keyword = ""
        keywords = []
        sql = ""
        for keyword_type in keyword_types:
            if keyword_type == "directly_keyword":
                keyword_temp = entity_dict.get('disease')[0]
                if keyword_temp in self.disease_wds:
                    keyword = keyword_temp
                    keywords.append(keyword)
                # 用户输入的疾病可能是别名，查询
                else:
                    sql = "MATCH (m:Disease)-[r:alias_is]->(n:Alias) where n.name = '{0}' return m.name".format(keyword_temp)
                    res = self.g.run(sql).data()
                    keyword = res[0]['m.name']
                    keywords.append(keyword)
                # 确定疾病后 添加疾病所在大类
                sql = "MATCH (m:Disease)-[r:belongs_to]->(n:Disease_Kind) where m.name = '{0}' return n.name".format(keyword)
                res = self.g.run(sql).data()
                if(len(res)!=0):
                    keyword = res[0]['n.name']
                    keywords.append(keyword)
            elif keyword_type == "symptom_keyword":
                keyword_temp = entity_dict.get('symptom')[0]
                sql = "MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where n.name = '{0}' return m.name".format(keyword_temp)
                res = self.g.run(sql).data()
                if (len(res) != 0):
                    keyword = res[0]['m.name']
                    keywords.append(keyword)
            elif keyword_type == "drug_keyword":
                keyword_temp = entity_dict.get('drug')[0]
                sql = "MATCH (m:Drug)-[r:to_cure]->(n:Disease) where m.name = '{0}' return n.name".format(keyword_temp)
                res = self.g.run(sql).data()
                if (len(res) != 0):
                    keyword = res[0]['n.name']
                    keywords.append(keyword)
        return keywords
if __name__ == '__main__':
    handler = KeywordExtraction()
    while 1:
        question = input('用户：')
        keyword = handler.keyword_extraction_main(question)
        print('关键词：',keyword)
        # print('cypher：',answer)
