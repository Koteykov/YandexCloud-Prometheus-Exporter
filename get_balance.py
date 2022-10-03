import requests
import json

params = {
    'username': 'test',
    'password': 'test'
}
url = 'https://api.reg.ru/api/regru2/user/get_balance'
res = requests.post(url, params=params)
jres = res.json()

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)
# jprint(jres)

print(jres['answer']['prepay'])
