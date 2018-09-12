from ttfidf import tfidf
import re
import csv
import nltk
import string
from collections import Counter
from random import random
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

TOP_N_DOCS = 5
TEST_PERCENT_SPLIT = 10

class TestTFIDF:
    def __init__(self):
        self.table = tfidf()
        self.stemmer = PorterStemmer()

    def run_tfidf(self):
        svc_req_list = list(self.read_svc_req_csv('analytics/service_requests_Train-test_set.csv'))
        #RANDOMISE
        #svc_req_list = sorted(svc_req_list, key=lambda x: random())
        train_count = len(svc_req_list) * (100 - TEST_PERCENT_SPLIT) // 100
        print train_count
        self.sr_id_rescode_mapping = self.create_mapping(svc_req_list)
        svc_req_train, svc_req_test = svc_req_list[:train_count], svc_req_list[train_count:]
        for svc_req in svc_req_train:
            self.load_svc_req_item(svc_req)
        num_accurate = 0
        for svc_req in svc_req_test:
            num_accurate += self.test_step(svc_req)
        test_count = len(svc_req_list) - train_count
        accuracy = num_accurate / float(test_count)
        print 'total test count: {}'.format(test_count)
        print 'total accurate: {}'.format(num_accurate)
        print 'accuracy: {}'.format(accuracy)

    def test_step(self, svc_req):
        symptom = self.clean_symptom_text(svc_req['symptom'])
        similar_docs = []
        for doc in self.table.similarities(symptom):
            if doc[1] > 0.0: # THIS IS THRESHOLD
                similar_docs.append(doc)
        similar_docs_ranked = sorted(similar_docs, key=self.takeSecond)
        if similar_docs_ranked > TOP_N_DOCS:
            top_docs = similar_docs_ranked[-TOP_N_DOCS:] # THIS IS THRESHOLD
        else:
            top_docs = similar_docs_ranked

        #VOTING FUNCTION 1: test if actual resolution code is present in top docs
        print "\n"
        print "ACTUAL RESCODE: " + svc_req['final_rescode']
        for doc in top_docs:
            print self.sr_id_rescode_mapping[doc[0]]
            if self.sr_id_rescode_mapping[doc[0]] == svc_req['final_rescode']:
                return 1
        return 0

        # VOTING FUNCTION 2: test if top resolution code in top docs is the actual resolution code
        # rescode_counter = Counter()
        # for doc in top_docs:
        #     doc_rescode = self.sr_id_rescode_mapping[doc[0]]
        #     rescode_counter[doc_rescode] += 1
        # top_rescode = rescode_counter.most_common(1)
        # if top_rescode and top_rescode[0][0] == svc_req['final_rescode']:
        #     return 1
        # return 0


    def takeSecond(self, elem):
        return elem[1]

    def create_mapping(self, svc_req_list):
        mapping = {}
        for svc_req in svc_req_list:
            mapping[svc_req['sr_id']] = svc_req['final_rescode']
        return mapping

    def load_svc_req_item(self, svc_req):
        symptom = self.clean_symptom_text(svc_req['symptom'])
        self.table.add_document(svc_req['sr_id'], symptom)

    def clean_symptom_text(self, symptom):
        symptom = re.sub(r'\w*\d\w*', '', symptom).strip().lower()
        #symptom = [x for x in symptom if x.isalpha()]
        tokens = nltk.word_tokenize(symptom)
        remove_words = ['image:none-none-none', 'none-none-none']
        stemmed_tokens = [self.stemmer.stem(token) or token for token in tokens if token not in remove_words]
        final_tokens = set(stemmed_tokens) - set(stopwords.words('english'))
        final_tokens_2 = final_tokens - set(string.punctuation)
        # FIXME OTHER STEPS: SPELLING CHECKER & ISALPHA & REMOVE MORE WORDS & REGEX REMOVE IMAGE:XX
        return final_tokens_2

    def read_svc_req_csv(self, fname):
        with open(fname) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            is_first = True
            for row in csv_reader:
                if is_first:
                    is_first = False
                    continue
                yield {
                    'sr_id': row[0],
                    'timestamp': row[1],
                    'final_rescode': row[2],
                    'symptom': row[3],
                }

if __name__ == "__main__":
    dl = TestTFIDF()
    dl.run_tfidf()
