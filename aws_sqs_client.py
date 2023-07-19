from datetime import datetime
import aws_signature_v4
import requests
import url_utility
import config
import json

class SqsClient:
    def __init__(self, accessKey, accessSecret, accNumber, region):
        self.region = region
        self.accessKey = accessKey
        self.accessSecret = accessSecret
        self.baseUrl = f'http://sqs.{self.region}.amazonaws.com/{accNumber}/'

    def getMessage(self, queueName):
        isoDateTime = getCurrentTimeISO()
        url = self.baseUrl + f'{queueName}' + "?Action=ReceiveMessage&MaxNumberOfMessages=1"        
        headers = self.buildHeaders(isoDateTime)
              
        authHeader = aws_signature_v4.buildAuthHeader("GET", url, self.region, "sqs", isoDateTime, "", self.accessKey, self.accessSecret)
        headers.update(authHeader)       
        
        responseJson = self.sendGetRequest(url, headers=headers)
        messages = responseJson["ReceiveMessageResponse"]["ReceiveMessageResult"]["messages"]
        if (not messages or len(messages) == 0):
            return None
        

        receiptHandle = messages[0]["ReceiptHandle"]
        print(f'ReceiptHandle: {receiptHandle}')

        self.deleteMessage(queueName, receiptHandle)
        #Process deletion of message

    def deleteMessage(self, queueName, receipt_handle):
        delete_url = self.baseUrl + f'{queueName}' + "?Action=DeleteMessage"

        body = {
            "ReceiptHandle": receipt_handle
        }

        isoDateTime = getCurrentTimeISO()
        headers = self.buildHeaders(isoDateTime)

        authHeader = aws_signature_v4.buildAuthHeader("POST", delete_url, self.region, "sqs", isoDateTime, json.dumps(body), self.accessKey, self.accessSecret)
        headers.update(authHeader) 
        
        response = self.sendPostRequest(delete_url, headers, body)
        print(response)
   
    def sendGetRequest(self, url, headers):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else: 
            return None
        
    def sendPostRequest(self, url, headers, body):
        response = requests.post(url, headers=headers, data=body)
        return response

    def buildHeaders(self, isoDateTime):
        headers = {
            'Host': url_utility.get_host(self.baseUrl),
            'X-Amz-Date': isoDateTime,
            'Accept': "application/json",
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        return headers

def getCurrentTimeISO():
        isoDateTime = datetime.utcnow().strftime("%Y%m%dT%H%M%S") + 'Z'
        return isoDateTime
 
client = SqsClient(config.AWS_KEY, config.AWS_SECRET, config.AWS_ACCOUNT_NUMBER, config.AWS_REGION)
client.getMessage(config.AWS_QUEUENAME)
#print(x)