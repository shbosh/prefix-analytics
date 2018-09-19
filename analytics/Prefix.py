#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import ast
import os
import json
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.externals import joblib
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

from preprocess import Preprocess


class Prefix:
    def __init__(self):
        self.preprocessor = Preprocess()

    def run_model(self, data, modelmap={}):
        data_json = json.loads(data)
        ensemble = self._import_model()
        headers = self._import_headers()

        tmp_dict = {}
        terms = self.preprocessor.process_text(data_json['data']['symptom'])
        terms += data_json['data']['error_codes']
        for header in headers:
            found = False
            for term in terms:
                if term == header:
                    tmp_dict[header] = 1
                    found = True
            if not found:
                tmp_dict[header] = 0

        df = pd.DataFrame([tmp_dict], columns=tmp_dict.keys())
        prediction_classes = ensemble.classes_[np.argsort(ensemble.predict_proba(df), axis=1)[:,-3:]][0][::-1].tolist()
        prediction_prob = ensemble.predict_proba(df)[0][np.argsort(ensemble.predict_proba(df), axis=1)[:, -3:]][0][::-1].tolist()

        res_dict = {
            'predictions': [{'label': prediction_classes[id],'proba': prediction_prob[id]} for id in range(0,3)]
        }
        return json.dumps(res_dict)

    def _import_model(self):
        return joblib.load(open('analytics/full_model.pkl', 'rb'))

    def _import_headers(self):
        with open('analytics/headers.txt', 'r') as file:
            headers = eval(file.read())
            return headers


# if __name__ == "__main__":
#     demo = Prefix()
#     json_input = json.dumps({
#         "data": {
#             'sr_id': '123456',
#             'error_codes': [],
#             'symptom': 'Getting feedback in the control room from the scan room despite the volume being all the way down. Image:NONE-NONE-NONE',
#         }
#     })
#     results = demo.run_model(json_input)
#     print(results)
