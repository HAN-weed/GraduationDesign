class QuestionPaser:

    '''构建实体节点'''
    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)

        return entity_dict

    '''解析主函数'''
    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        question_types = res_classify['question_types']
        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []
            if question_type == 'disease_symptom':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'symptom_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('symptom'))

            elif question_type == 'disease_cause':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_characteristic':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_prevent':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_cureway':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            # elif question_type == 'food_not_disease':
            #     sql = self.sql_transfer(question_type, entity_dict.get('food'))
            #
            # elif question_type == 'food_do_disease':
            #     sql = self.sql_transfer(question_type, entity_dict.get('food'))
            #
            # elif question_type == 'disease_drug':
            #     sql = self.sql_transfer(question_type, entity_dict.get('disease'))
            #
            # elif question_type == 'drug_disease':
            #     sql = self.sql_transfer(question_type, entity_dict.get('drug'))
            #
            # elif question_type == 'disease_check':
            #     sql = self.sql_transfer(question_type, entity_dict.get('disease'))
            #
            # elif question_type == 'check_disease':
            #     sql = self.sql_transfer(question_type, entity_dict.get('check'))
            #
            # elif question_type == 'disease_prevent':
            #     sql = self.sql_transfer(question_type, entity_dict.get('disease'))
            #
            # elif question_type == 'disease_lasttime':
            #     sql = self.sql_transfer(question_type, entity_dict.get('disease'))
            #
            # elif question_type == 'disease_cureway':
            #     sql = self.sql_transfer(question_type, entity_dict.get('disease'))
            #
            # elif question_type == 'disease_cureprob':
            #     sql = self.sql_transfer(question_type, entity_dict.get('disease'))
            #
            # elif question_type == 'disease_easyget':
            #     sql = self.sql_transfer(question_type, entity_dict.get('disease'))
            #
            elif question_type == 'disease_introduction':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            if sql:
                sql_['sql'] = sql

                sqls.append(sql_)

        return sqls

    '''针对不同的问题，分开进行处理'''

    def sql_transfer(self, question_type, entities):
        if not entities:
            return []

        # 查询语句
        sql = []

        # 查询疾病有哪些症状
        if question_type == 'disease_symptom':
            sql = ["MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 查询症状会导致哪些疾病
        elif question_type == 'symptom_disease':
            sql = ["MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where n.name = '{0}' return m.name, r.name, n.name".format(i)
                for i in entities]
        # 查询疾病的原因
        elif question_type == 'disease_cause':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cause".format(i) for i in entities]
        # 查询疾病的特点
        elif question_type == 'disease_characteristic':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.characteristic".format(i) for i in entities]
        # 查询疾病的预防措施
        elif question_type == 'disease_prevent':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.prevent".format(i) for i in entities]
        # 查询疾病的治疗手段
        elif question_type == 'disease_cureway':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cure".format(i) for i in entities]

        # 没有特殊点明要查询什么，返回简介
        elif question_type == 'disease_introduction':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.introduction".format(i) for i in entities]
        return sql

if __name__ == '__main__':
    handler = QuestionPaser()
