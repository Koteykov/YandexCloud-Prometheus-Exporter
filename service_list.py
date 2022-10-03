import requests
import json

params = {
    'username': 'test',
    'password': 'test'
}
url = 'https://api.reg.ru/api/regru2/service/get_list'
res = requests.post(url, params=params)
jres = res.json()

for each in jres['answer']['services']:
    print(each['dname'])
    print(each['expiration_date'])
