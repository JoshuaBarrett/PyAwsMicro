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
        isoDateTime = getCurrentTimeISO()
        url = self.baseUrl + f'{queueName}' + "?Action=ReceiveMessage&MaxNumberOfMessages=1"        
        headers = self.buildHeaders(isoDateTime)
              
        authHeader = aws_signature_v4.buildAuthHeader("GET", url, self.region, "sqs", isoDateTime, "", self.accessKey, self.accessSecret)
        headers.update(authHeader)       
        
        responseJson = self.sendGetRequest(url, headers=headers)
        messages = responseJson["ReceiveMessageResponse"]["ReceiveMessageResult"]["messages"]
        if (not messages or len(messages) == 0):
            return None      

        #Lets delete the message
        receiptHandle = messages[0]["ReceiptHandle"]
        responseStatus = self.deleteMessage(queueName, receiptHandle)
        print(responseStatus)

        messageBody = messages[0]["Body"]
        return messageBody


    def deleteMessage(self, queueName, receipt_handle):       
        delete_url = self.baseUrl + f'{queueName}' + "?Action=DeleteMessage"        
        isoDateTime = getCurrentTimeISO()
        
        #calculate prehex payload
        prehashedPayload = f'ReceiptHandle={url_utility.urlEncode(receipt_handle)}'
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
        print(authHeader)
        
        params = { 
            "ReceiptHandle": receipt_handle
        }

        print(requests.post(delete_url, headers=headers, data=params))

        return ""

   
    def sendGetRequest(self, url, headers):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else: 
            return None
        
    def sendPostRequest(self, url, headers):
        response = requests.post(url, headers=headers)
        return response
    
    def sendPostRequest(self, url, headers, params):
        response = requests.post(url, headers=headers, params=params)
        return response

    def buildHeaders(self, isoDateTime):
        headers = {
            'host': url_utility.get_host(self.baseUrl),
            'X-Amz-Date': isoDateTime,
            'Accept': "application/json",
        }

        return headers

def getCurrentTimeISO():
        isoDateTime = datetime.utcnow().strftime("%Y%m%dT%H%M%S") + 'Z'
        return isoDateTime
        #return "20230721T221001Z"

client = SqsClient(config.AWS_KEY, config.AWS_SECRET, config.AWS_ACCOUNT_NUMBER, config.AWS_REGION)
x = client.deleteMessage(config.AWS_QUEUENAME, "AQEBRzfvEH8SLrpEHXRKX1q8sBfcToihEQGkPoe+uL3Tf9vBlfJ2pJxVeaynbGLCKzwxgvgPBfPvxg2WFCxd5LtNG1liS3eeQWkzfPpci/5LJkDU8LhP8xgRpG4ADw9OXqNGEaYP7I1cgrTS6xcxTDI9ktFkq1JWb8FGlZEguw4eb9DN6ITCSf+NQUqzHYBC6hc4ZZRbcJtHg6WhnP3BtDVQ3kdHiyb+LruYURshmFYZs0q5eV82qF4cE9IpanCF2Zq5zJ75A6Spx74/WGGb6ceftF6GWS0mcv/vHKJMPlPkw9nB+3UBx0tHAVoS0hreOvGx5TR2NK9j97QbCvrjxtFdnkxvbkaGmAn4Cz3k05IFCH6Dr54jZ7a7sBi/tN7m7Z0puFCvzLtyUsNhsKFg5QDNdw==")
#print(x)                                       AQEBNcvkQFA%252FHbek4vgSaumj5NWhAgkcZ4Id11J2gsqsBU4HeANDi6lykCgKfg7SwmEr08NZ8rMh3DoRwtftbVRRUbXE3fgPwnB%252FNx1dd7ceDWBh3gwzeQ3TCXp7TxacDa4BUliRNuBa%252F3DeDR8vRix3tKXvrczqQq59%252B2CwFSO8FdcBaNsoHLvuV3lIkPIpVbPEiggyjPBNUH1bs1xUJ1bXasQRnkG9Dh%252BU%252B978TFVcqJsy%252B%252FK4BQJYQ0uhLu%252FyLfKWO00obYty3GV6zLIVNbUUfAXAQ5RSyaZx4SDBLAqI%252FDhkZZa6LGx7bpcTZBfYN5uGHBEOZiLSb50JEw%252BtRIEu%252BJ67g3bycGHTujqSQUyB%252BFtWjZElCwJrVJLKIdj7lkQSg5l2ZJmtuZpN%252BAgYhjrC1A%253D%253D






