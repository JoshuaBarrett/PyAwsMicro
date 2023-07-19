import hasher
import url_utility

def buildAuthHeader(method, fullUrl, region, service, isoDateTime, payload, awsKey, awsSecret):
    signature = buildAuthSignature(method, fullUrl, region, service, isoDateTime, payload, awsSecret)
    authorisationHeaderValue = f'AWS4-HMAC-SHA256 Credential={awsKey}/{isoDateTime[0:8]}/{region}/sqs/aws4_request, SignedHeaders=host;x-amz-date, Signature={signature}'
    return { 'Authorization': authorisationHeaderValue }

def buildAuthSignature(method, fullUrl, region, service, isoDateTime, payload, awsSecret): 
    canonicalRequest = buildCanonicalRequest(method, fullUrl, isoDateTime, payload)  
    hashedCanonicalRequest = hasher.basicHash(canonicalRequest).hex()
    
    stringToSign = f'AWS4-HMAC-SHA256\n{isoDateTime}\n{isoDateTime[0:8]}/{region}/{service}/aws4_request\n{hashedCanonicalRequest}'
    
    kSigning = buildKSigning(awsSecret, isoDateTime[0:8], region, service)
    signature = hasher.keyedHash(kSigning, stringToSign)
    return signature.hex()

def buildCanonicalRequest(httpMethod, fullUrl, isoDateTime, payload):
    host = url_utility.get_host(fullUrl)
    canonicalUri = url_utility.get_uri(fullUrl)
    canonicalQueryString = url_utility.get_query_string(fullUrl)    
    hashedPayload = hasher.basicHash(payload).hex()
    canonicalHeaders=f'host:{host}\nx-amz-date:{isoDateTime}\n'
    signedHeaders = "host;x-amz-date"
    return f'{httpMethod}\n{canonicalUri}\n{canonicalQueryString}\n{canonicalHeaders}\n{signedHeaders}\n{hashedPayload}'

def buildKSigning(awsSecret, shortDate, region, service):
    kDate = hasher.keyedHash("AWS4"+awsSecret, shortDate)
    kRegion = hasher.keyedHash(kDate, region)
    kService = hasher.keyedHash(kRegion, service)
    kSigning = hasher.keyedHash(kService, "aws4_request")
    return kSigning