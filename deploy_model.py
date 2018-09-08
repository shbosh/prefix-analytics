import requests

class PredixClient:
    def __init__(self):
        #self.token = self.get_token()
        self.token = '''eyJhbGciOiJSUzI1NiIsImtpZCI6IlU5V0VXIiwidHlwIjoiSldUIn0.eyJqdGkiOiJkZTFmN2Q5NTVmYWM0ZjNlYjAzYTBkNThjODM0YjVhNiIsInN1YiI6ImFwcF9jbGllbnRfaWQiLCJzY29wZSI6WyJjbGllbnRzLnJlYWQiLCJ1YWEucmVzb3VyY2UiLCJvcGVuaWQiLCJ1YWEubm9uZSIsInByZWRpeC1hc3NldC56b25lcy4yNmJkZTcxYy1kYWFmLTRjNzItOTc1NS1iYjIxZjU4YzJkNWIudXNlciIsImh0dHBzOi8vcHJlZGl4LWFuYWx5dGljcy1jYXRhbG9nLXJlbGVhc2UucnVuLmF3cy11c3cwMi1wci5pY2UucHJlZGl4LmlvIiwiYW5hbHl0aWNzLnpvbmVzLjdkNGM0ZTNmLWI1YTUtNDFkOC05MThkLTliMzNmOGI0ZGJiMi51c2VyIl0sImNsaWVudF9pZCI6ImFwcF9jbGllbnRfaWQiLCJjaWQiOiJhcHBfY2xpZW50X2lkIiwiYXpwIjoiYXBwX2NsaWVudF9pZCIsImdyYW50X3R5cGUiOiJjbGllbnRfY3JlZGVudGlhbHMiLCJyZXZfc2lnIjoiM2Y0NDAyNWIiLCJpYXQiOjE1MzYyNjU0MDQsImV4cCI6MTUzNjMwODYwNCwiaXNzIjoiaHR0cHM6Ly8xNGMwZDI3Yy1iY2RmLTQ0MzItYmUyYy1hMDk2ZDNiYjk0NzcucHJlZGl4LXVhYS5ydW4uYXdzLXVzdzAyLXByLmljZS5wcmVkaXguaW8vb2F1dGgvdG9rZW4iLCJ6aWQiOiIxNGMwZDI3Yy1iY2RmLTQ0MzItYmUyYy1hMDk2ZDNiYjk0NzciLCJhdWQiOlsiaHR0cHM6Ly9wcmVkaXgtYW5hbHl0aWNzLWNhdGFsb2ctcmVsZWFzZS5ydW4uYXdzLXVzdzAyLXByLmljZS5wcmVkaXgiLCJjbGllbnRzIiwidWFhIiwib3BlbmlkIiwiYW5hbHl0aWNzLnpvbmVzLjdkNGM0ZTNmLWI1YTUtNDFkOC05MThkLTliMzNmOGI0ZGJiMiIsInByZWRpeC1hc3NldC56b25lcy4yNmJkZTcxYy1kYWFmLTRjNzItOTc1NS1iYjIxZjU4YzJkNWIiLCJhcHBfY2xpZW50X2lkIl19.UgIYUDFYD8otYQ6m3NQ0SJaTPTQng1iMAmGakdJ0CHwdetcTf8P95F4FPOiezrdDuS8AUcAyij4FvvS4WD1Lbaw_HHkgG62rA8dWm4vO65luFXx3Kj7N4rFWI3hkDPo8Kz9tOt4w7tIBgoOjlXANH3CP6FbB-yyGmEk3ISaO8PNL5pCJyQA-f8RpVcuwSQJHV5spozqXteLqSSAUNBX_JbQ57MUZ3MYPUkjS1kZ37lybLkwYUTjhNLRhQwqsUxap0pov_CoxIIUkaRivVMsiPSSHzliRQM0R9i9daFS6_oZgd6OIyR48zY_wOZkl7TM7kOgpJTTFQ24B5-mCC_gooA
        '''
        self.tenant_id = '7d4c4e3f-b5a5-41d8-918d-9b33f8b4dbb2'
        self.catalog_uri = 'https://predix-analytics-catalog-release.run.aws-usw02-pr.ice.predix.io'
        self.config_uri = 'https://predix-analytics-config-release.run.aws-usw02-pr.ice.predix.io'
        self.execution_uri = 'https://predix-analytics-execution-release.run.aws-usw02-pr.ice.predix.io'
        self.scheduler_uri = 'https://predix-scheduler-service-release.run.aws-usw02-pr.ice.predix.io'
        self.monitoring_uri = 'https://predix-analytics-monitoring-release.run.aws-usw02-pr.ice.predix.io'
        self.catalogEntryId = '95ba454d-0956-43ed-8f05-8363876ed7e3'
        self.validationId = '5616bb47-0553-42d5-9a02-10bb60746199'

    def get_token(self):
        res = requests.post('https://14c0d27c-bcdf-4432-be2c-a096d3bb9477.predix-uaa.run.aws-usw02-pr.ice.predix.io/oauth/token',
            headers={
                'Authorization': 'Basic YXBwX2NsaWVudF9pZDpwcmVmaXh3b3Jr',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data='grant_type=client_credentials'
        )
        return res.json()['access_token']

    def create_analytic(self):
        pass

    def create_artifact(self):
        pass

    def check_deployment_status(self):
        pass

    def validate_analytic(self):
        pass

    def deploy_analytic(self):
        pass

    def execute_analytic(self):
        pass

    def delete_analytic(self):
        pass


if __name__ == "__main__":
    pc = PredixClient()
    print(pc.token)
