import requests
import datetime
import time
import argparse
from prometheus_client import start_http_server, Gauge

parser = argparse.ArgumentParser(description='Enter username and password')

parser.add_argument('-u',
                    '--username',
                    type=str,
                    help='param = username',
                    default='test')
parser.add_argument('-p',
                    '--password',
                    type=str,
                    help='param = password',
                    default='test')
parser.add_argument('-w',
                    '--webport',
                    type=int,
                    help='param = Port for internal web server, Def=8100',
                    default=8100)

args = parser.parse_args()

params = {
    'username': args.username,
    'password': args.password
}

# Check if there are any unpayed bills
def bills_state():
    if len(jres_bills['answer']['bills']) == 0:
        return 0
    else:
        return 1

start_http_server(args.webport)

reg_ru_balance_state_histogram = Gauge('reg_ru_balance_state',
                                       'reg.ru balance status in currency RUR',
                                       ['site'])
reg_ru_services_state_histogram = Gauge('reg_ru_services_state',
                                        'reg.ru services expiration date',
                                        ['site', 'serviceid', 'name'])
reg_ru_bills_state_histogram = Gauge('reg_ru_bills_state',
                                     'reg.ru bills status, 0 = you have no unpaid bills, 1 = there are unpaid bills',
                                     ['site'])
try:
    while True:
        jres_services = requests.post('https://api.reg.ru/api/regru2/service/get_list', params=params).json()
        jres_balance = requests.post('https://api.reg.ru/api/regru2/user/get_balance', params=params).json()
        jres_bills = requests.post('https://api.reg.ru/api/regru2/bill/get_not_payed', params=params).json()

        reg_ru_balance_state_histogram_launch = reg_ru_balance_state_histogram.labels(site='reg.ru')
        reg_ru_bills_state_histogram_launch = reg_ru_bills_state_histogram.labels(site='reg.ru')

        reg_ru_balance_state_histogram_launch.set(jres_balance['answer']['prepay'])
        reg_ru_bills_state_histogram_launch.set(bills_state())

        service_list = [(s['servtype'], s['dname'], s['expiration_date']) for s in jres_services['answer']['services']]

        for e in service_list:
            try:
                date_obj = datetime.datetime.strptime(e[2], '%Y-%m-%d')
            except:
                date_obj = datetime.datetime.strptime('2000-01-01', '%Y-%m-%d')
            date = datetime.datetime.timestamp(date_obj)
            if (datetime.datetime.now().timestamp() - date) < 7777000:
                reg_ru_services_state_histogram_launch = reg_ru_services_state_histogram.labels(site='reg.ru',
                                                                                                serviceid=e[0],
                                                                                                name=e[1])
                reg_ru_services_state_histogram_launch.set(date)
        time.sleep(86400)
except:
    print(jres_services, '\n', jres_balance, '\n', jres_bills)
