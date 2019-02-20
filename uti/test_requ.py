# -*- coding: utf-8 -*
import requests

# data={
#         'columns':'["col1","col2"]',
#         'ogCode':'953d626e-6eb6-4d57-b7bb-3156af88be3f',
#         'processId':"8",
#         'resourceName':"卫计委数据",
#         'resourceId':"2018da",
#         'visitCount':'5'
#        }
# html=requests.request(method="POST",url="http://localhost:8000/api/datalink/",data=data)
# print(1)
#html=requests.request(method="GET",url="http://www.baidu.com")
# print(html.text)

# data = {
#           "apiKey": "string",
#           "fileId": 0,
#           "interfaceAddress": "string",
#           "procId": 81
#         }
#
# html = requests.request(method="POST", url="http://192.168.31.137:8080/thirdParty/shareExchange/successFeedback", data=data)
# print(html.text)
#


import requests


# url = 'http://127.0.0.1:8000/api/getDatalinkUrls/'
# with open('E:/贵阳项目/海云接口文档/aa.txt') as fp:
#     data = fp.read()
# post = {
#     'file': data
# }
# resp = requests.post(url, data=post)

url = 'http://192.168.25.40:8000/new_interface/get_firstdir'
headers = {'content-type': 'application/x-www-form-urlencoded'}
data = {"depart":"贵州省大数据局"}
html = requests.request(method="POST", headers=headers, url = url)
print(html.text)