
import os
import ahocorasick

class QuestionClassifier:
    def __init__(self):
        #特征词文件的绝对文件夹路径
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        # 定义特征词路径
        self.disease_path = os.path.join(cur_dir,'dict/disease.txt')
        self.symptom_path = os.path.join(cur_dir,'dict/symptom.txt')
        self.disease_kind_path = os.path.join(cur_dir,'dict/disease_kind.txt')
        self.drug_path = os.path.join(cur_dir,'dict/drug.txt')
        self.pathogen_path = os.path.join(cur_dir,'dict/pathogen.txt')
        self.deny_path = os.path.join(cur_dir,'dict/deny.txt')
        self.alias_path = os.path.join(cur_dir,'dict/alias.txt')

        # 加载特征词
        self.disease_wds = [i.strip() for i in open(self.disease_path,encoding='utf-8') if i.strip()]
        self.symptom_wds = [i.strip() for i in open(self.symptom_path,encoding='utf-8') if i.strip()]
        self.disease_kind_wds = [i.strip() for i in open(self.disease_kind_path,encoding='utf-8') if i.strip()]
        self.drug_wds = [i.strip() for i in open(self.drug_path,encoding='utf-8') if i.strip()]
        self.pathogen_wds = [i.strip() for i in open(self.pathogen_path,encoding='utf-8') if i.strip()]
        self.alias_wds = [i.strip() for i in open(self.alias_path,encoding='utf-8') if i.strip()]

        self.region_wds = set(self.disease_wds+self.symptom_wds+self.disease_kind_wds+self.drug_wds+self.pathogen_wds+self.alias_wds)
        self.deny_wds = [i.strip() for i in open(self.deny_path, encoding='utf-8') if i.strip()]


        # 问句疑问句
        self.disease_qwds = ['疾病']
        self.alias_is_qwds = ['别名','别名是','又叫','又称为','又叫做','别称']
        self.symptom_qwds = ['症状', '表征', '现象', '症候', '表现']
        self.characteristic_qwds = ['特点','后果']
        self.easy_get_qwds = ['易感','易感期','什么时候','容易感染']
        self.cause_qwds = ['原因', '成因', '为什么', '怎么会', '怎样才', '咋样才', '怎样会', '如何会', '为啥', '为何', '如何才会', '怎么才会', '会导致',
                           '会造成']
        self.drug_qwds = ['药', '药品', '用药', '药剂']
        self.prevent_qwds = ['预防', '防范', '抵制', '抵御', '防止', '躲避', '逃避', '避开', '免得', '逃开', '避开', '避掉', '躲开', '躲掉', '绕开',
                             '怎样才能不', '怎么才能不', '咋样才能不', '咋才能不', '如何才能不',
                             '怎样才不', '怎么才不', '咋样才不', '咋才不', '如何才不',
                             '怎样才可以不', '怎么才可以不', '咋样才可以不', '咋才可以不', '如何可以不',
                             '怎样才可不', '怎么才可不', '咋样才可不', '咋才可不', '如何可不']
        self.cureway_qwds = ['怎么治疗', '如何医治', '怎么医治', '怎么治', '怎么医', '如何治', '医治方式', '疗法', '咋治', '怎么办', '咋办', '咋治']
        self.belong_qwds = ['属于什么种类', '属于', '什么种类', '种类']
        self.include_qwds = ['包含', '包括', '拥有']
        self.cure_qwds = ['治疗什么','治疗', '治啥', '治疗啥', '医治啥', '治愈啥', '主治啥', '主治什么', '有什么用', '有何用', '用处', '用途',
                          '有什么好处', '有什么益处', '有何益处', '用来', '用来做啥', '用来作甚', '需要', '要','能做什么']
        self.pathogen_qwds = ['病原','病原体','病原体是','由什么造成']
        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_wds))
        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict()
        print('model init finished ......')

        return

    '''问答类主函数'''
    def classify(self,question):
        data = {}
        # 问句过滤
        medical_dict = self.check_medical(question)
        if not medical_dict:
            return {}
        data['args'] = medical_dict
        # 收集问句当中涉及到的实体类型
        types = []
        for type_ in medical_dict.values():
            types += type_

        question_type = 'others'
        question_types = []

        ## 症状
        if self.check_words(self.symptom_qwds,question) and ('disease' in types):
            question_type = 'disease_symptom'
            question_types.append(question_type)

        if self.check_words(self.symptom_qwds, question) and ('symptom' in types):
            question_type = 'symptom_disease'
            question_types.append(question_type)

        ## 疾病原因
        if self.check_words(self.cause_qwds,question) and ('disease' in types) :
            question_type = 'disease_cause'
            question_types.append(question_type)
        ## 疾病易感染期
        if self.check_words(self.easy_get_qwds,question) and ('disease' in types) :
            question_type = 'disease_easy_get'
            question_types.append(question_type)

        ## 疾病特点
        if self.check_words(self.characteristic_qwds,question) and ('disease' in types) :
            question_type = 'disease_characteristic'
            question_types.append(question_type)
        ## 疾病预防措施
        if self.check_words(self.prevent_qwds,question) and ('disease' in types) :
            question_type = 'disease_prevent'
            question_types.append(question_type)
        ## 疾病治疗方法
        if self.check_words(self.cureway_qwds,question) and ('disease' in types) :
            question_type = 'disease_cureway'
            question_types.append(question_type)

        ## 别名
        if self.check_words(self.alias_is_qwds,question) and ('disease' in types):
            question_type = 'disease_alias'
            question_types.append(question_type)

        if self.check_words(self.alias_is_qwds,question) and ('alias_is' in types):
            question_type = 'alias_disease'
            question_types.append(question_type)

        ## 种类
        if self.check_words(self.belong_qwds,question) and ('disease' in types):
            question_type = 'disease_disease_kind'
            question_types.append(question_type)

        if self.check_words(self.include_qwds,question) and ('belongs_to' in types):
            question_type = 'disease_kind_disease'
            question_types.append(question_type)

        ## 推荐药品
        if self.check_words(self.drug_qwds,question) and ('disease' in types):
            question_type = 'disease_drug'
            question_types.append(question_type)

        if self.check_words(self.cure_qwds,question) and ('drug' in types):
            question_type = 'drug_disease'
            question_types.append(question_type)
        ## 病原体
        if self.check_words(self.pathogen_qwds, question) and ('disease' in types):
            question_type = 'disease_pathogen'
            question_types.append(question_type)

        if self.check_words(self.cause_qwds, question) and ('pathogen' in types):
            question_type = 'pathogen_disease'
            question_types.append(question_type)

        # 若没有查到相关的外部查询信息，就将该疾病的描述信息返回
        if question_types == [] and 'disease' in types:
            question_types = ['disease_introduction']

        # 若没有查到相关的外部查询信息，就将该疾病的描述信息返回
        if question_types == [] and 'symptom' in types:
            question_types = ['symptom_desc']

        # 将多个分类结果进行合并处理， 组装成一个字典
        data['question_types'] = question_types

        return data

    '''构造actree'''
    def build_actree(self,wordlist):
        actree = ahocorasick.Automaton()
        for index,word in enumerate(wordlist):
            actree.add_word(word,(index,word))
        actree.make_automaton()
        return actree

    '''构造词对应的类型'''
    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_wds:
            wd_dict[wd] = []
            if wd in self.disease_wds:
                wd_dict[wd].append('disease')
            if wd in self.symptom_wds:
                wd_dict[wd].append('symptom')
            if wd in self.characteristic_qwds:
                wd_dict[wd].append('characteristic')
            if wd in self.prevent_qwds:
                wd_dict[wd].append('prevent')
            if wd in self.cureway_qwds:
                wd_dict[wd].append('cureway')
            if wd in self.alias_wds:
                wd_dict[wd].append('alias_is')
            if wd in self.easy_get_qwds:
                wd_dict[wd].append('easy_get')
            if wd in self.cause_qwds:
                wd_dict[wd].append('cause')
            if wd in self.drug_wds:
                wd_dict[wd].append('drug')
            if wd in self.disease_kind_wds:
                wd_dict[wd].append('belongs_to')
            if wd in self.cure_qwds:
                wd_dict[wd].append('cure')
            if wd in self.pathogen_wds:
                wd_dict[wd].append('pathogen')

        return wd_dict

    '''问句过滤'''
    def check_medical(self,question):
        region_wds = []
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)

        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i:self.wdtype_dict.get(i) for i in final_wds}

        return final_dict

    '''基于特征词进行分类'''
    def check_words(self,wds,sentence):
        for wd in wds:
            if wd in sentence:
                return True
        return False

if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        print(data)
