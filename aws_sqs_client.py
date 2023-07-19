from datetime import datetime
import aws_signature_v4
import requests
import url_utility
import config

class SqsClient:
    def __init__(self, accessKey, accessSecret, accNumber, region):
        self.region = region
        self.accessKey = accessKey
        self.accessSecret = accessSecret
        self.baseUrl = f'http://sqs.{self.region}.amazonaws.com/{accNumber}/'

    def getMessage(self, queueName):
        isoDateTime = getCurrentTimeISO()
        url = self.baseUrl + f'{queueName}/' + "?Action=ReceiveMessage&MaxNumberOfMessages=1"        
        headers = self.buildHeaders(isoDateTime)
              
        authHeader = aws_signature_v4.buildAuthHeader("GET", url, self.region, "sqs", isoDateTime, "", self.accessKey, self.accessSecret)
        headers.update(authHeader)       
        
        responseData = self.sendGetRequest(url, headers=headers)
        

        return responseData

   
    def sendGetRequest(self, url, headers):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else: 
            return None     

    def buildHeaders(self, isoDateTime):
        headers = {
            'Host': url_utility.get_host(self.baseUrl),
            'X-Amz-Date': isoDateTime,
            'Accept': "application/json",
        }

        return headers

def getCurrentTimeISO():
        isoDateTime = datetime.utcnow().strftime("%Y%m%dT%H%M%S") + 'Z'
        return isoDateTime
 
client = SqsClient(config.AWS_KEY, config.AWS_SECRET, config.AWS_ACCOUNT_NUMBER, config.AWS_REGION)
x = client.getMessage(config.AWS_QUEUENAME)
print(x)