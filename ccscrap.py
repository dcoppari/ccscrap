#!/usr/bin/python3

import sys
import os
import requests
from requests.exceptions import HTTPError
from datetime import date, timedelta, datetime

api_url     = "https://api.ap.crosschexcloud.com/api"
login_url   = api_url + "/login/chklogin"
company_url = api_url + "/company/select"
report_url  = api_url + "/record/grid"

token=None

s = requests.session()

def main(argv):
    global login, report_payload

    try:
        login()

        report()

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')

    except Exception as err:
        print(f'Other error occurred: {err}')


def login():
    global token

    required = ["CROSSCHEXCLOUD_EMAIL", "CROSSCHEXCLOUD_PASSWORD", "CROSSCHEXCLOUD_COMPANY_ID"]

    for env in required:
        if env not in os.environ:
            raise EnvironmentError(f'Failed to load {env} Environment Variables')
        elif not os.environ[env]:
            raise EnvironmentError(f'{env} Environment Variables is empty')

    login_payload = {
        "email": os.environ['CROSSCHEXCLOUD_EMAIL'],
        "password": os.environ['CROSSCHEXCLOUD_PASSWORD'],
    }

    response = s.post(login_url,data=login_payload )
    response.raise_for_status()
    payload = response.json()

    token = payload["data"]["token"]

    company_payload = {
        "company_id": os.environ['CROSSCHEXCLOUD_COMPANY_ID']
    }

    response = s.post(company_url,data=company_payload, headers={"x-token": token} )
    response.raise_for_status()
    payload = response.json()

    token = payload["data"]["token"]

def report():
    global token

    today=datetime.today().strftime("%Y-%m-%d")

    report_payload = {
        "department_id": "",
        "startdate": today,
        "enddate": today,
        "keyword": "",
        "order_col": "checktime",
        "order_dir": "DESC",
        "page": 1,
        "perPage": 200
    }

    response = s.post(report_url,data=report_payload, headers={"x-token": token} )
    response.raise_for_status()
    payload = response.json()

    sqlDump(time_entries=payload["data"]["list"])

def sqlDump(time_entries):
    for time_entry in time_entries:
        row = { 'tarjeta':   time_entry['workno'],
                'fechaChar': time_entry['date'],
                'crc':       time_entry['time'] + ':00',
                'reloj':     time_entry['device'],
                'codigo':    time_entry['id'],
                'fecha':     datetime.strptime(time_entry['date'], "%d/%m/%Y").strftime("%Y-%m-%d"),
                'hora':      time_entry['time'] + ':00',
        }

        columns = ', '.join("`" + str(x) + "`" for x in row.keys())
        values = ', '.join("'" + str(x) + "'" for x in row.values())

        sql = "INSERT IGNORE INTO %s ( %s ) VALUES ( %s );" % ('RH_FICHADAS', columns, values)

        print(sql)

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)




if __name__ == "__main__":
   main(sys.argv[1:])
