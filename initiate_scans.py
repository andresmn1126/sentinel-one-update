import requests
from os import getenv

api_token = "ApiToken " + getenv('SENTINEL_ONE_API')
headers = {'Authorization': api_token}


def get_sites():
    url = 'https://usea1-007.sentinelone.net/web/api/v2.1/sites'
    res = requests.get(url, headers=headers, params={'limit': 1000})
    json_res = res.json()
    sites_ids = [site['id'] for site in json_res['data']['sites']]
    return sites_ids


def initiate_scans(site_ids):
    url = 'https://usea1-007.sentinelone.net/web/api/v2.1/agents/actions/initiate-scan'
    json_data = {'filter': {'siteIds': site_ids}}
    try:
        res = requests.post(url, headers=headers, json=json_data)
        affected = res.json()['data']['affected']
        print(f"Scan initiated on {affected} agents")
    except requests.exceptions.HTTPError as e:
        print(e)


def main():
    sites = get_sites()
    initiate_scans(sites)


if __name__ == '__main__':
    main()