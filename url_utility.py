from urllib.parse import quote_plus 

def get_host(url):
    url = url.split("://", 1)[-1]    
    host = url.split("/", 1)[0]
    return host

def get_uri(url):
    url = url.split("://", 1)[-1]
    uri = url.split("/", 1)[-1]
    uri = uri.split("?", 1)[0]
    return "/" + uri

def get_query_string(url):
    url = url.split("://", 1)[-1]
    query_string = url.split("?", 1)[-1]
    return query_string

def urlEncode(strData):
    return quote_plus(strData)