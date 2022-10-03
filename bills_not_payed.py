import requests
import json

params = {
    'username': 'test',
    'password': 'test'
}
url = 'https://api.reg.ru/api/regru2/bill/get_not_payed'
res = requests.post(url, params=params)
jres = res.json()

# for each in jres['answer']['bills']:
#    jprint(each)

if len(jres['answer']['bills']) == 0:
    print('0')
else:
    print('1')
