import requests
from django.test import TestCase

# Create your tests here.

def test(fileId):
    fileId = str(fileId)
    url = 'http://59.215.191.23:8080/components/anon/selectFileInfoById/'+fileId
    method = 'GET'
    res = requests.request(url=url,
                           method=method)
    filePath = res.json()
    # print(filePath)
    filePath1 = filePath["result"]['fileServerPath']
    print(filePath1)





test(830)


