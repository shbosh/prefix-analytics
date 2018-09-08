import csv
import psycopg2
from sklearn.externals import joblib

class DBLoader:
    def __init__(self):
        # connect to db
        try:
            self.conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password=''")
            self.cur = self.conn.cursor()
        except:
            print "I am unable to connect to the database"

    def load_to_db(self):
        # svc_req_list = list(self.read_svc_req_csv('analytics/service_requests_Train-test_set.csv'))
        # for svc_req in svc_req_list:
        #     self.load_svc_req_item(svc_req)
        error_log_list = joblib.load('SR_with_syslog_error_code.joblib')
        for error_log in error_log_list:
            self.load_error_log_item(error_log)
            break
        self.conn.close()

    def load_svc_req_item(self, sr):
        try:
            self.cur.execute("""INSERT INTO service_request(sr_id, symptom, final_rescode, req_status, req_timestamp) VALUES (%s, %s, %s, %s, %s);""", (sr['sr_id'], sr['symptom'], sr['final_rescode'], 'RESOLVED', sr['timestamp']))
            self.conn.commit()
        except psycopg2.IntegrityError:
            print 'sr_id: {} already in db'.format(sr['sr_id'])
            self.conn.rollback()

    def load_error_log_item(self, el):
        try:
            self.cur.execute("""INSERT INTO error_Log(error_code, error_timestamp, sr_id) VALUES (%s, %s, %s);""", (el['error_codes'], el['log_timestamp'], el['sr_id']))
            self.conn.commit()
        except psycopg2.IntegrityError:
            print 'sr_id: {} already in db'.format(sr['sr_id'])
            self.conn.rollback()

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
    dl = DBLoader()
    dl.load_to_db()
