import requests

host_name = 'http://127.0.0.1:5000'


def get_eachball_data_from_api(matchid, from_over, to_over):
    url = host_name + f'/api/cricket/eachballdata/{matchid}/{from_over}/{to_over}'
    json_data = requests.get(url)
    json_data = json_data.json()
    return json_data


def get_all_seasons_from_api():
    url = host_name + f'/api/cricket/seasons'
    json_data = requests.get(url).json()
    return json_data


def get_all_matchids_from_api(season):
    if '/' in season:
        season = season.replace('/', '-')
    url = host_name + f'/api/cricket/matchids/{season}'
    json_data = requests.get(url).json()
    return json_data


def get_match_data_from_api(matchid):
    url = host_name + f'/api/cricket/matches/{matchid}'
    json_data = requests.get(url)
    json_data = json_data.json()
    return json_data
