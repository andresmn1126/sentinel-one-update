import requests
from os import getenv
from packaging import version
from operator import itemgetter

api_token = "ApiToken " + getenv('SENTINEL_ONE_API')
headers = {'Authorization': api_token}


def get_os_package(os_type):
    url = 'https://usea1-007.sentinelone.net/web/api/v2.1/update/agent/packages'
    res = requests.get(url, headers=headers, params={'limit': 1000}).json()['data']
    packages = [i for i in res if i['osType'] == os_type and i['status'] == 'ga' and i['fileExtension'] != '.exe']
    sorted_packages = sorted(packages, key=itemgetter('version'), reverse=True)
    return sorted_packages[0]


def get_outdated_agents(os_type, ver):
    url = 'https://usea1-007.sentinelone.net/web/api/v2.1/agents'
    res = requests.get(url, headers=headers, params={'limit': 1000}).json()
    agents = []
    ids = [a for a in res['data'] if version.parse(a['agentVersion']) < version.parse(ver)]
    agents.extend(ids)
    while res['pagination']['nextCursor']:
        next_cursor = res['pagination']['nextCursor']
        res = requests.get(url, headers=headers, params={'cursor': next_cursor, 'limit': 1000}).json()
        ids = [a for a in res['data'] if a['osType'] == os_type and version.parse(a['agentVersion']) < version.parse(ver)]
        agents.extend(ids)
    return agents


def update_agents(agents, ver_id):
    url = 'https://usea1-007.sentinelone.net/web/api/v2.1/agents/actions/update-software'
    for a in agents:
        try:
            json_data = {'data': {'packageId': ver_id, 'isScheduled': False}, 'filter': {'uuid': a['uuid']}}
            update = requests.post(url, headers=headers, json=json_data)
            print(f"Update on {a['computerName']} under {a['siteName']} successfully triggered")
        except:
            print(update.status_code)


def main():
    win_id = get_os_package('windows')
    mac_id = get_os_package('macos')
    win_agents = get_outdated_agents('windows', win_id['version'])
    mac_agents = get_outdated_agents('macos', mac_id['version'])
    update_agents(win_agents, win_id['id'])
    update_agents(mac_agents, mac_id['id'])


if __name__ == '__main__':
    main()
