from question_classifier import *
from question_parser import *
from answer_search import *

'''问答类'''
class ChatGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()

    def chat(self,sentence):
        answer = '"很抱歉没有查询到相关信息"'
        res_classify = self.classifier.classify(sentence)
        if not res_classify:
            return answer
        res_sql = self.parser.parser_main(res_classify)
        print(res_sql)
        final_answer = self.searcher.search_main(res_sql)
        if not final_answer:
            return answer
        else:
            return final_answer

if __name__ == '__main__':
    handler = ChatGraph()
    while 1:
        question = input('用户：')
        answer = handler.chat(question)
        print('回答：',answer)
        # print('cypher：',answer)
