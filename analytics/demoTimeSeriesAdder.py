import pandas as pd
import numpy as np
import requests
import ast
import pickle
from sklearn.feature_extraction import text
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.externals import joblib
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


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
        clean_el_df = self.clean_error_logs(error_log_df)
        combined_df = self.combine_df(clean_sr_df, clean_el_df)

        features_train, features_test, labels_train, labels_test = train_test_split(combined_df,combined_df.Resolution_Code,test_size=0.2,random_state=1)
        ## Drop y from features
        features_train_dropped = features_train.drop('Resolution_Code', 1)
        features_test = features_test.drop('Resolution_Code', 1)

        ## Build random forest classifier
        classifier = RandomForestClassifier()
        classifier.fit(features_train_dropped, labels_train)

        ## Accuracy
        rfc_predictions = classifier.predict(features_test)
        print accuracy_score(labels_test, rfc_predictions)
        # save classifier as pickle
        joblib.dump(classifier, 'model.pkl')
        # upload to blobstore


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
        ## merge back with other columns
        Xtrain = svc_request_df.symptom.reset_index()
        final = pd.concat([Xtrain, count_vect_df], axis=1).set_index('index')
        ## merge with resolution_codes
        final_cleaned = pd.merge(final, svc_request_df, 'left', left_index=True, right_index=True)
        return final_cleaned

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
        return e4

    def combine_df(self, sr_df, el_df):
        final_df = pd.merge(sr_df, el_df, 'left', on = 'sr_id').fillna(-999).drop('symptom_x', 1).drop('symptom_y', 1).drop('sr_id', 1).drop('Created_Date', 1)
        return final_df

    def run_model(self, data):
        classifier = joblib.load('model.pkl')
        # create a df with all the features
        #classifier.predict()



if __name__ == "__main__":
    demo = demoTimeSeriesAdder()
    demo.train_model()
    #demo.run_model()
