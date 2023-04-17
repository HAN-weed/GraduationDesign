from py2neo import Graph

class AnswerSearcher:
    def __init__(self):
        self.g = Graph("bolt://localhost:7687",auth = ('neo4j','123456'))
        self.num_limit = 20
    '''执行cypher查询语句，并返回相应结果'''
    def search_main(self,sqls):
        final_answers = []
        imgs_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            answers = []
            for query in queries:
                res = self.g.run(query).data()
                answers+=res
            print(answers)
            final_answer,imgs_answers= self.answer_prettify(question_type,answers)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers,imgs_answers
    '''根据对应的question_type，调用相应的回复模板'''
    def answer_prettify(self,question_type,answers):
        final_answer = []
        imgs_answers =[]
        if not answers:
            return ''
        if question_type == 'disease_symptom':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的症状包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        if question_type == 'symptom_disease':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{1}可能是{0}的症状'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        ## 疾病的原因
        if question_type == 'disease_cause':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['m.cause']
            final_answer = '{1}的原因包括：{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        ## 疾病的易感期
        if question_type == 'disease_easy_get':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['m.easy_get']
            final_answer = '{1}的易感期：{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        ## 疾病的特点
        if question_type == 'disease_characteristic':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['m.introduction']
            final_answer = '{1}的特点包括：{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        ## 疾病的预防措施
        if question_type == 'disease_prevent':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['m.prevent']
            final_answer = '{1}的预防措施：{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        ## 疾病的治疗方案
        if question_type == 'disease_cureway':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['m.cure']
            final_answer = '{1}的治疗方式：{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        ## 疾病别名
        if question_type == 'disease_alias':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}又叫做：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        if question_type == 'alias_disease':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{1}是{0}的别名'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        ## 疾病种类
        if question_type == 'disease_disease_kind':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}属于：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        if question_type == 'disease_kind_disease':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        ## 疾病推荐药品
        if question_type == 'disease_drug':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}推荐用药：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        if question_type == 'drug_disease':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{1}能治疗：{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        ## 疾病病原体
        if question_type == 'disease_pathogen':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的致病病原为：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        if question_type == 'pathogen_disease':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{1}会导致：{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        # 没有特殊点明要查询什么，返回简介
        if question_type == 'disease_introduction':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['m.introduction']
            final_answer = '{1}的简单介绍：{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        if question_type == 'symptom_desc':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['m.detail']
            final_answer = '{1}的简单介绍：{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        print(answers)
        if question_type == 'disease_img' and answers:
            print('================')
            print(answers)
            print('================')
            imgs_answers = answers

        return final_answer,imgs_answers

if __name__ == '__main__':
    searcher = AnswerSearcher()
