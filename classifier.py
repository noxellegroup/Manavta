import os
import ahocorasick
import pandas as pd

class QuestionClassifier:
    def __init__(self):    
        self.disease_df = pd.read_csv('classifier_data/disease.csv')
        self.department_df = pd.read_csv('classifier_data/department.csv')
        self.symptoms_df = pd.read_csv('classifier_data/symptoms.csv')

        self.disease_wds= self.disease_df['Diseases'].tolist()
        self.department_wds= self.department_df['Departments'].tolist()
        self.symptom_wds= self.symptoms_df['Symptoms'].tolist()
        self.region_words = set(self.department_wds + self.disease_wds + self.symptom_wds)

        self.region_tree = self.build_actree(list(self.region_words))

        self.wdtype_dict = self.build_wdtype_dict()

        self.symptom_qwds = ['symptom', 'symptoms', 'characterization', 'characterizations', 'phenomenon', 'phenomena']
        self.cause_qwds = ['reason', 'reasons', 'cause', 'causes']
        self.accompany_qwds = ['complication', 'complications', 'concurrent', 'occur', 'happen together', 'happens together', 'occur together', 'occurs together', 'appear together', 'appears together', 'together', 'accompany', 'accompanies', 'follow', 'follows', 'coexist', 'coexists']
        self.prevent_qwds = ['prevention', 'prevent', 'resist', 'guard', 'against','escape', 'avoid', 'how can I not', 'how not to', 'why not', 'how to prevent']
        self.cureway_qwds = ['treat', 'heal', 'heals', 'cure', 'cures', 'how to treat', 'how to heal', 'how to cure', 'treatment', 'therapy']
        self.belong_qwds = ['what belongs to', 'belong', 'belongs','section','what section', 'department']

    def classify(self, question):
        data = {}
        question2 = question.lower()
        medical_dict = self.check_medical(question2)
        if not medical_dict:
            return {}
        data['args'] = medical_dict

        types = []
        for type_ in medical_dict.values():
            types += type_
        question_type = 'others'

        question_types = []

        if self.check_words(self.symptom_qwds, question2) and ('disease' in types):
            question_type = 'disease_symptom'
            question_types.append(question_type)

        if self.check_words(self.symptom_qwds, question2) and ('symptom' in types):
            question_type = 'symptom_disease'
            question_types.append(question_type)

        if self.check_words(self.cause_qwds, question2) and ('disease' in types):
            question_type = 'disease_cause'
            question_types.append(question_type)

        if self.check_words(self.accompany_qwds, question2) and ('disease' in types):
            question_type = 'disease_accompany'
            question_types.append(question_type)

        if self.check_words(self.prevent_qwds, question2) and 'disease' in types:
            question_type = 'disease_prevent'
            question_types.append(question_type)
            
        if self.check_words(self.cureway_qwds, question2) and 'disease' in types:
            question_type = 'disease_cure'
            question_types.append(question_type)

        if self.check_words(self.belong_qwds, question2) and 'disease' in types:
            question_type = 'disease_department'
            question_types.append(question_type)

        if question_types == [] and 'disease' in types and 'symptom' not in types:
            question_types = ['disease_desc']

        if question_types == [] and 'symptom' in types:
            question_types = ['symptom_disease']

        data['question_types'] = question_types

        return data

    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.disease_wds:
                wd_dict[wd].append('disease')
            if wd in self.department_wds:
                wd_dict[wd].append('department')
            if wd in self.symptom_wds:
                wd_dict[wd].append('symptom')
        return wd_dict

    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    def check_medical(self, question):
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

    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False


def intent_identifier(question):
    handler = QuestionClassifier()
    data = handler.classify(question)
    return data