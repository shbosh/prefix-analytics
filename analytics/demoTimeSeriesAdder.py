import pandas as pd
import numpy as np
import requests
import ast
from sklearn.feature_extraction import text
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn import metrics


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
        clean_sr_df = self.clean_svc_request(svc_request_df)
        clean_el_df = self.clean_error_log(error_log_df)


    def load_data_from_files(self):
        svc_request_df = pd.read_csv("service_requests_Train-test_set.csv")
        error_log_df = pd.read_csv("test_error_code.csv")
        return svc_request_df, error_log_df


    def load_data_from_db(self):
        pass

    def clean_sr_df(self):
        pass

    def clean_error_log(self):
        pass



if __name__ == "__main__":
    demo = demoTimeSeriesAdder()
    demo.train_model()
