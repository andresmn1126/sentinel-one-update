import requests
from os import getenv
from packaging import version
from operator import itemgetter

api_token = "ApiToken " + getenv('SENTINEL_ONE_API')
headers = {'Authorization': api_token}


def get_os_package(os_type):
    url = 'https://usea1-007.sentinelone.net/web/api/v2.1/update/agent/packages'
    res = requests.get(url, headers=headers, params={'limit': 1000}).json()['data']
    packages = [i for i in res if i['osType'] == os_type and i['status'] == 'ga' and i['fileExtension'] != '.msi']
    sorted_packages = sorted(packages, key=itemgetter('version'), reverse=True)
    return sorted_packages[0]


def get_outdated_agents(os_type, ver):
    s = requests.session()
    url = 'https://usea1-007.sentinelone.net/web/api/v2.1/agents'
    res = s.get(url, headers=headers, params={'limit': 1000}).json()
    agents = [a for a in res['data'] if version.parse(a['agentVersion']) < version.parse(ver)]
    while res['pagination']['nextCursor']:
        next_cursor = res['pagination']['nextCursor']
        res = s.get(url, headers=headers, params={'cursor': next_cursor, 'limit': 1000}).json()
        more = [a for a in res['data'] if a['osType'] == os_type and version.parse(a['agentVersion']) < version.parse(ver)]
        agents.extend(more)
    return agents


def update_agents(agents, ver_id):
    url = 'https://usea1-007.sentinelone.net/web/api/v2.1/agents/actions/update-software'
    for a in agents:
        try:
            json_data = {'data': {'packageId': ver_id, 'isScheduled': True}, 'filter': {'uuid': a['uuid']}}
            update = requests.post(url, headers=headers, json=json_data)
            update.raise_for_status()
            print(f"Update on {a['computerName']} under {a['siteName']} successfully triggered")
        except requests.exceptions.HTTPError as e:
            print(e)


def main():
    os_types = ('windows', 'macos')
    winid, macid = map(get_os_package, os_types)
    winagents, macagents = map(get_outdated_agents, os_types, (winid['version'], macid['version']))
    update_agents(winagents, winid['id'])
    update_agents(macagents, macid['id'])


if __name__ == '__main__':
    main()
