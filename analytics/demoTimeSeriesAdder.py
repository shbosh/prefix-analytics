import pandas as pd
import numpy as np
import requests
import ast
from sklearn.feature_extraction import text
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

class demoTimeSeriesAdder:
    def __init__(self):
        print "Create machine learning model"

    def add2NumberArrays(self, data, modelmap = {}):
        threshold = float(modelmap['threshold']) if len(modelmap) > 0 else None
        data_json = json.loads(data)
        numberArray1 = data_json['data']['time_series']['numberArray1']
        numberArray2 = data_json['data']['time_series']['numberArray2']
        sum = []
        for i in range(len(numberArray1)):
            result = numberArray1[i] + numberArray2[i]
            if (threshold is not None and result > threshold):
                sum.append(-1)
            else:
                sum.append(numberArray1[i] + numberArray2[i])

        timestamps = data_json['data']['time_series']['time_stamp']

        return json.dumps( \
            {
                "data":
                    {
                        "time_series":
                            {
                                "time_stamp": timestamps,
                                "sum": sum
                            }
                    }
            })

    def train_model(self):
        # get data into dataframe
        svc_request_df, error_log_df = self.load_data_from_files()
        clean_sr_df = self.clean_svc_requests(svc_request_df)
        #clean_el_df = self.clean_error_logs(error_log_df)
        #combined_df = self.combine_df(clean_sr_df, clean_el_df)

    def load_data_from_files(self):
        svc_request_df = pd.read_csv("service_requests_Train-test_set.csv")
        error_log_df = pd.read_csv("test_error_code.csv")
        return svc_request_df, error_log_df

    def load_data_from_db(self):
        pass

    def clean_svc_requests(self, svc_request_df):
        stop = text.ENGLISH_STOP_WORDS
        stopwords = r'\b(?:{})\b'.format('|'.join(stop))

        remove_words = ['imagenonenonenone', '^image', 'cst', 'cd', 'image:none-none-none']
        remove_words = r'\b(?:{})\b'.format('|'.join(remove_words))

        svc_request_df['symptom'] = svc_request_df['symptom'] \
            .apply(lambda x: x.replace('[^\w\s]','') \
                    .lower() \
                    .replace(stopwords, '') \
                    .replace('\d+', '') \
                    .replace(remove_words, '') \
            )
        # pivot words
        # print svc_request_df.symptom
        vect = CountVectorizer()
        X = vect.fit_transform(svc_request_df['symptom'])
        count_vect_df = pd.DataFrame(X.todense(), columns=vect.get_feature_names())
        print count_vect_df

    def clean_error_logs(self, error_log_df):
        # remove non-numeric error codes
        error_log_df['Numeric'] = error_log_df['error_codes'].apply(lambda s: str(s).isdigit())
        e1 = error_log_df[error_log_df['Numeric'] == True]
        # pivot error codes
        e2 = e1.groupby('sr_id')['error_codes'].apply(set).apply(list)
        e3 = pd.DataFrame({'sr_id':e2.index, 'error_codes':e2.values})
        mlb = MultiLabelBinarizer()
        e4 = e3.join(pd.DataFrame(mlb.fit_transform(e3.pop('error_codes')),
                          columns=mlb.classes_,
                          index=e3.index))
        print e4
        return e4


if __name__ == "__main__":
    demo = demoTimeSeriesAdder()
    demo.train_model()
