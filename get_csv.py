import requests
import os
from datetime import datetime
from pathlib import Path
import csv


api_token = "ApiToken " + os.getenv('SENTINEL_ONE_API')
CMS_SITE_ID = os.getenv('CMS_SITE_ID')
headers = {'Authorization': api_token}
download_dir = f'{Path.home()}/sentinel-one/downloads/'
now = datetime.now().strftime("%m-%d-%Y")


def export_agents_to_csv():
    url = 'https://usea1-007.sentinelone.net/web/api/v2.1/export/agents'
    res = requests.get(url, headers=headers, params={'siteIds': [CMS_SITE_ID]})
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    with open(f'{download_dir}CMS-CO_S1_Master_{now}.csv', 'w') as org:
        org.write(res.text)
    return res.text


def format_csv():
    with open(f'{download_dir}CMS-CO_S1_Master_{now}.csv', 'r') as org:
        reader = csv.reader(org)

        with open(f'{download_dir}CMS-CO_S1_ScanStatus_{now}.csv', 'w') as modified:
            writer = csv.writer(modified)
            for r in reader:
                writer.writerow((r[0], r[22]))


def main():
    export_agents_to_csv()
    format_csv()


if __name__ == '__main__':
    main()