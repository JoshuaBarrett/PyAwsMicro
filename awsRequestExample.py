import uhashlib
import requests
import config

def makeHash(inputStr):
    return uhashlib.sha256(inputStr.encode()).digest().hex()

def makeKeyedHash(data, key):
    return uhashlib.sha256(data.encode(), key.encode()).digest().hex()

def hmac_sha256(key_bytes, data_bytes):
    block_size = 64  # HMAC block size (in bytes)
    
    # Key padding: If the key is longer than block_size, hash it; otherwise, pad with zeros
    if len(key_bytes) > block_size:
        key_bytes = uhashlib.sha256(key_bytes).digest()
    key_bytes = key_bytes.ljust(block_size, b'\x00')

    # Inner and outer paddings for the key
    inner_key_pad = bytes([x ^ 0x36 for x in key_bytes])
    outer_key_pad = bytes([x ^ 0x5C for x in key_bytes])

    # Calculate inner and outer hash digests
    inner_digest = uhashlib.sha256(inner_key_pad + data_bytes).digest()
    outer_digest = uhashlib.sha256(outer_key_pad + inner_digest).digest()

    # Return the HMAC digest as a hexadecimal string
    
    return outer_digest


key=config.AWS_KEY
secret=config.AWS_SECRET
             
dateStrFull="20230718T234657Z"
dateStrShort=dateStrFull[0:8]
region="eu-west-1"
service="sqs"
host="sqs.eu-west-1.amazonaws.com"
url="http://sqs.eu-west-1.amazonaws.com/725813574532/RemoteQueue?Action=ReceiveMessage&MaxNumberOfMessages=1"

#Canonical Values
httpMethod="GET"
canonicalUri="/725813574532/RemoteQueue"
canonicalQueryString="Action=ReceiveMessage&MaxNumberOfMessages=1"
canonicalHeaders=f'host:sqs.eu-west-1.amazonaws.com\nx-amz-date:{dateStrFull}\n'
signedHeaders="host;x-amz-date"
hashedPayload="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

canonicalRequest = f'{httpMethod}\n{canonicalUri}\n{canonicalQueryString}\n{canonicalHeaders}\n{signedHeaders}\n{hashedPayload}'
hashedCanonicalRequest = makeHash(canonicalRequest)
print(canonicalRequest)
print(f'HashedCanonicalRequest\n{hashedCanonicalRequest}\n')


stringToSign=f'AWS4-HMAC-SHA256\n{dateStrFull}\n{dateStrShort}/eu-west-1/sqs/aws4_request\n{hashedCanonicalRequest}'
print(f'String to sign \n{stringToSign}\n')

kDate = hmac_sha256(f'AWS4{secret}'.encode("utf-8"), dateStrShort.encode("utf-8"))
kRegion = hmac_sha256(kDate, region.encode("utf-8"))
kService = hmac_sha256(kRegion, service.encode("utf-8"))
kSigning = hmac_sha256(kService, "aws4_request".encode("utf-8"))
signature = hmac_sha256(kSigning, stringToSign.encode("utf-8"))
print(signature.hex())


headers = {
        'Host': host,
        'X-Amz-Date': dateStrFull,
        'Accept': "application/json",
        'Authorization': f'AWS4-HMAC-SHA256 Credential={key}/{dateStrShort}/eu-west-1/sqs/aws4_request, SignedHeaders=host;x-amz-date, Signature={signature.hex()}'
    }

response = requests.get(url, headers=headers)
print (response)
#messages = response.json()["ReceiveMessageResponse"]["ReceiveMessageResult"]["messages"]
#if len(messages) > 0:
#    print(messages[0]["Body"])




