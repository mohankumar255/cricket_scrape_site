import time
import threading,concurrent.futures
from requests.auth import HTTPBasicAuth
import requests

def check_fsb_feed(match_event_id):
    feed_url=f'https://betlion-api.fsbtech.com/fsb-api-rest/bet/event/{match_event_id}.json?markets=true&detail=1x2'
    url = requests.get(feed_url, auth=HTTPBasicAuth('betlionapi', ']}Mbp7UGBm~7xh&E'))
    resp=url.json()
    values=resp['response']['category'][0]['subcat'][0]['event'][0]['market'][0]['selection']
    status_of_odds=[]
    for i in values:
        status_of_odds.append(i['active'])
    return status_of_odds


def create_urls(site_name,sport_name,league_name):
    site_name=site_name.lower()
    sport_url=[]
    if 'betlion' in site_name:
        userid='betlionapi'
        password=']}Mbp7UGBm~7xh&E'
        sport_url=f'https://betlion-api.fsbtech.com/fsb-api-rest/bet/category/{sport_name}.json'
        league_url=f'https://betlion-api.fsbtech.com/fsb-api-rest/bet/category/{sport_name}/{league_name}.json'
    elif 'betyetu'  in site_name:
        password='M2b1m^ba1&ISGSJZ'
        userid='betyetu-mz'
        sport_url=f'https://betyetu-mz-api.fsbtech.com/fsb-api-rest/bet/category/{sport_name}.json'
        league_url=f'https://betyetu-mz-api.fsbtech.com/fsb-api-rest/bet/category/{sport_name}/{league_name}.json'
    elif 'mkekabet' in site_name:
        password = 'M2b1m^ba1&ISGSJZ'
        userid = 'betyetu-mz'
        sport_url = f'https://betyetu-mz-api.fsbtech.com/fsb-api-rest/bet/category/{sport_name}.json'
        league_url = f'https://betyetu-mz-api.fsbtech.com/fsb-api-rest/bet/category/{sport_name}/{league_name}.json'
    elif 'playabet'  in site_name:
        password='ZMGHqkSq8muhNnHY'
        userid='playabetapi'
        sport_url=f'https://playabet-api.fsbtech.com/fsb-api-rest/bet/category/{sport_name}.json'
        league_url=f'https://playabet-api.fsbtech.com/fsb-api-rest/bet/category/{sport_name}/{league_name}.json'
    elif 'parimatch' in site_name:
        password = 'ZMGHqkSq8muhNnHY'
        userid = 'playabetapi'
        sport_url = f'https://playabet-api.fsbtech.com/fsb-api-rest/bet/category/{sport_name}.json'
        league_url = f'https://playabet-api.fsbtech.com/fsb-api-rest/bet/category{sport_name}/{league_name}.json'
    return [sport_url,league_url,userid,password]


def get_league_matches(site_name,sport_name,league_name):
    all_details = create_urls(site_name,sport_name,league_name)
    try:
        url = requests.get(all_details[1], auth=HTTPBasicAuth(all_details[2], all_details[3]))
        resp = url.json()
        response_code = url.status_code
        if response_code == 200:
            print('connected to Feed')
        else:
            print(response_code)
            print('not connected to Feed')
        events=[]
        event_ids=resp['response']['category'][0]['subcat'][0]['event']
        for id in event_ids:
            if id['state'] == 'IN_PLAY':
                if id['virtual']:
                    pass
                elif id['displayed']:
                    events.append([id['id'],id['scheduledStart']])
                else:
                    pass
    except:
        pass
    return events


def live_matches_all_event_ids(site_name,sport_name,league_name):
    all_details = create_urls(site_name,sport_name,league_name)
    url = requests.get(all_details[0], auth=HTTPBasicAuth(all_details[2], all_details[3]))
    resp = url.json()
    event_ids = resp['response']['category'][0]['subcat']
    league_names = []
    for league_name in event_ids:
        name = league_name['ref']
        league_names.append(name)
    event_ids = []
    st = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results=[executor.submit(get_league_matches,site_name,sport_name,league_names[i]) for i in range(len(league_names))]
        d=[]
        for f in concurrent.futures.as_completed(results):
            if len(f.result()) > 0:
                for event_id in f.result():
                    event_ids.append(event_id)
    return event_ids


# print(live_matches_all_event_ids('betlion','SOCCER',''))

