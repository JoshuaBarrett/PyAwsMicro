from datetime import datetime
import aws_signature_v4
import requests
import url_utility
import config
import json
import hasher
from urllib.parse import quote_plus

class SqsClient:
    def __init__(self, accessKey, accessSecret, accNumber, region):
        self.region = region
        self.accessKey = accessKey
        self.accessSecret = accessSecret
        self.baseUrl = f'http://sqs.{self.region}.amazonaws.com/{accNumber}/'

    def getMessage(self, queueName):
        url = self.baseUrl + f'{queueName}' + "?Action=ReceiveMessage&MaxNumberOfMessages=1&WaitTimeSeconds=10"
        isoDateTime = getCurrentTimeISO()
                
        headers = {
            'host': url_utility.get_host(self.baseUrl),
            'x-amz-date': isoDateTime,
        }

        emptyPayloadHashed = hasher.basicHash("").hex()
        authHeaderProto = aws_signature_v4.buildAuthHeaderProto("GET", url, self.region, "sqs", isoDateTime, headers, emptyPayloadHashed, self.accessKey, self.accessSecret)
        headers.update(authHeaderProto)     
        
        #return
        response = self.get(url, headers)
        if response.status_code != 200:
            return None
        
        messages = response.json()["ReceiveMessageResponse"]["ReceiveMessageResult"]["messages"]
        if (not messages or len(messages) == 0):
            return None
      
        #Lets delete the message
        receiptHandle = messages[0]["ReceiptHandle"]
        responseStatus = self.deleteMessage(queueName, receiptHandle)
        
        if responseStatus == 200:
            messageBody = messages[0]["Body"]     
            return messageBody
        
        return None

    def deleteMessage(self, queueName, receipt_handle):       
        delete_url = self.baseUrl + f'{queueName}' + "?Action=DeleteMessage"        
        isoDateTime = getCurrentTimeISO()
        
        #Build Params for request - Url encoding for values is handled by requests module
        params = { 
            "ReceiptHandle": receipt_handle
        }

        #calculate hash payload - values need to be pre url encoded
        prehashedPayload = aws_signature_v4.prepPayload(params)
        contentLength = len(prehashedPayload)
        hashedPayload = hasher.basicHash(prehashedPayload).hex()
        
        headers = {
            'content-length': str(contentLength),
            'content-type': "application/x-www-form-urlencoded",
            'host': url_utility.get_host(self.baseUrl),
            'x-amz-content-sha256': hashedPayload,
            'x-amz-date': isoDateTime,            
        }
             
        authHeader = aws_signature_v4.buildAuthHeaderProto("POST", delete_url, self.region, "sqs", isoDateTime, headers, hashedPayload, self.accessKey, self.accessSecret) 
        headers.update(authHeader)
        
        response = requests.post(delete_url, headers=headers, data=params)
        return response.status_code   
    
    def get(self, url, headers):
        headers.update({"accept": "application/json"})
        response = requests.get(url, headers=headers)
        return response

def getCurrentTimeISO():
        isoDateTime = datetime.utcnow().strftime("%Y%m%dT%H%M%S") + 'Z'
        return isoDateTime

client = SqsClient(config.AWS_KEY, config.AWS_SECRET, config.AWS_ACCOUNT_NUMBER, config.AWS_REGION)
x = client.getMessage(config.AWS_QUEUENAME)
print(x)







