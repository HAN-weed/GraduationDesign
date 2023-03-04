from py2neo import Graph

class AnswerSearcher:
    def __init__(self):
        self.g = Graph("bolt://localhost:7687",auth = ('neo4j','123456'))
        self.num_limit = 20
    '''执行cypher查询语句，并返回相应结果'''
    def search_main(self,sqls):
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            answers = []
            for query in queries:
                res = self.g.run(query).data()
                answers+=res
            final_answer = self.answer_prettify(question_type,answers)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers
    '''根据对应的question_type，调用相应的回复模板'''
    def answer_prettify(self,question_type,answers):
        final_answer = []
        if not  answers:
            return ''
        if question_type == 'disease_symptom':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的症状包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        if question_type == 'symptom_disease':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的症状包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        ## 疾病的原因
        if question_type == 'disease_cause':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['m.cause']
            final_answer = '{1}的原因包括：{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        ## 疾病的特点
        if question_type == 'disease_characteristic':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['m.characteristic']
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
        # 没有特殊点明要查询什么，返回简介
        if question_type == 'disease_introduction':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['m.introduction']
            final_answer = '{1}的简单介绍：{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        return final_answer

if __name__ == '__main__':
    searcher = AnswerSearcher()
