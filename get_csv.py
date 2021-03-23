import requests
from os import getenv
from datetime import datetime
import csv


api_token = "ApiToken " + getenv('SENTINEL_ONE_API')
CMS_SITE_ID = getenv('CMS_SITE_ID')
headers = {'Authorization': api_token}
now = datetime.now().strftime("%m-%d-%y")


def export_agents_to_csv():
    url = 'https://usea1-007.sentinelone.net/web/api/v2.1/export/agents'
    res = requests.get(url, headers=headers, params={'siteIds': [CMS_SITE_ID]})
    with open(f'CMS-CO_S1_Master_{now}.csv', 'w') as org:
        org.write(res.text)
    return res.text


def format_scan():
    with open(f'CMS-CO_S1_Master_{now}.csv', 'r') as org:
        reader = csv.reader(org)

        with open(f'CMS-CO_S1_ScanStatus_{now}.csv', 'w') as modified:
            writer = csv.writer(modified)
            for r in reader:
                writer.writerow((r[0], r[22]))


def main():
    export_agents_to_csv()
    format_scan()


if __name__ == '__main__':
    main()