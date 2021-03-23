import requests
from os import getenv

api_token = "ApiToken " + getenv('SENTINEL_ONE_API')
CMS_SITE_ID = getenv('CMS_SITE_ID')
headers = {'Authorization': api_token}


def initiate_scans():
    url = 'https://usea1-007.sentinelone.net/web/api/v2.1/agents/actions/initiate-scan'
    json_data = {'filter': {'siteIds': [CMS_SITE_ID]}}
    try:
        res = requests.post(url, headers=headers, json=json_data)
        affected = res.json()['data']['affected']
        print(f"Scan initiated on {affected} agents")
    except requests.exceptions.HTTPError as e:
        print(e)


def main():
    initiate_scans()


if __name__ == '__main__':
    main()