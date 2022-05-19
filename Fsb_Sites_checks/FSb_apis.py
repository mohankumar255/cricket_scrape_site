import json
import requests
from requests.auth import HTTPBasicAuth
import threading,concurrent.futures
import time


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
            if id['state'] == 'SCHEDULED':
                if id['virtual']:
                    pass
                elif id['displayed']:
                    events.append([id['id'],id['scheduledStart']])
                else:
                    pass
    except:
        pass
    return events


def scheduled_matches_in_fsb(site_name,sport_name,league_name):
    all_details = create_urls(site_name,sport_name,league_name)
    url = requests.get(all_details[0], auth=HTTPBasicAuth(all_details[2], all_details[3]))
    resp = url.json()
    print(resp)
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

def individual_event_feeds(site_name,event_id):
    if 'betlion' in site_name:
        userid = 'betlionapi'
        password=']}Mbp7UGBm~7xh&E'
        url=f'https://betlion-api.fsbtech.com/fsb-api-rest/bet/event/{event_id}.json'
    elif 'betyetu' in site_name:
        url =f'https://betyetu-mz-api.fsbtech.com/fsb-api-rest/bet/event/{event_id}.json'
    elif 'playabet':
        url=f'https://playabet-api.fsbtech.com/fsb-api-rest/bet/event/{event_id}.json'
        password = 'ZMGHqkSq8muhNnHY'
        userid = 'playabetapi'
    return [url,userid,password]


def each_event_market_names(site_name,sport_name,league_name,market_name,time_range):
    event_ids=scheduled_matches_in_fsb(site_name,sport_name,league_name)
    for eventid in event_ids:
        print(eventid)
        data_checks = individual_event_feeds(site_name, eventid[0])
        connect_url = requests.get(data_checks[0],auth=HTTPBasicAuth(data_checks[0],data_checks[1]))
        json_data = connect_url.json()
        data_1 = json_data['response']['category'][0]['subcat'][0]['event'][0]['market']
        list_of_events=[]
        for book in data_1:
            data_2 = book['name']
            if market_name in data_2:
                list_of_events.append(eventid)
    return list_of_events


# print(each_event_market_names('betlion','SOCCER','','Match Result','333'))
data_checks = individual_event_feeds('betlion',9664038)
connect_url = requests.get(data_checks[0],auth=HTTPBasicAuth(data_checks[0],data_checks[1]))
json_data = connect_url.json()
print(json_data)
#data_1 = json_data['response']['category'][0]['subcat'][0]['event'][0]['market']
