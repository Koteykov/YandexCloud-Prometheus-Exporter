import requests
import argparse
import time
import json
from prometheus_client import start_http_server, Gauge

parser = argparse.ArgumentParser(description='Enter webport and oauth token')
parser.add_argument('-w',
                    '--webport',
                    type=int,
                    help='param = Port for internal web server, Def=8100',
                    default=8100)
parser.add_argument('-o',
                    '--oauth',
                    type=str,
                    help='param = Oauth token for authorization',
                    default='test')
args = parser.parse_args()

start_http_server(args.webport)

YC_balance_state_histogram = Gauge('YC_balance_state',
                                   'YandexCloud balance status in currency RUR',
                                   ['site'])
try:
    while True:
        payload = json.dumps({"yandexPassportOauthToken": args.oauth})
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", 'https://iam.api.cloud.yandex.net/iam/v1/tokens', headers=headers, data=payload).json()

        iam = response['iamToken']

        headers = {'Authorization': 'Bearer ' + iam, 'Accept': '*/*'}
        jres_balance = requests.get('https://billing.api.cloud.yandex.net/billing/v1/billingAccounts/dn2525hf279h8uj4eqvn',
                                    headers=headers).json()
        YC_balance_state_histogram_launch = YC_balance_state_histogram.labels(site='YandexCloud')
        YC_balance_state_histogram_launch.set(jres_balance['balance'])
        time.sleep(86400)
except:
    print(jres_balance)
