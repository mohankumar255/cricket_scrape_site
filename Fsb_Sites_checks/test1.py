import threading,concurrent.futures
import datetime, time
import requests, json
from requests.auth import HTTPBasicAuth

sports_list = ['SOCCER','BASKETBALL','TENNIS','VOLLEYBALL','CRICKET','SNOOKER','BASEBALL','BOXING','MOTORSPORT']
sites_list = ['betlion','betyetu','playabet','parimatch']
#sports_list=['SOCCER']
#sites_list=['betlion']
times_list = []

def get_time_data(num):
    a1 = datetime.datetime.today()+datetime.timedelta(days=num)
    a2=a1.strftime('20%y:%m:%d 00:00:00')
    a3 = datetime.datetime.strptime(a2,'%Y:%m:%d %H:%M:%S')
    a4 = a3.timetuple()
    time_stamp = time.mktime(a4)
    return time_stamp


for i in range(6):
    times_list.append(get_time_data(i))


def create_urls(site_name,sport_name):
    site_name=site_name.lower()
    sport_url=[]
    if 'betlion' in site_name:
        userid='betlionapi'
        password=']}Mbp7UGBm~7xh&E'
        sport_url=f'https://betlion-api.fsbtech.com/fsb-api-rest/bet/category/{sport_name}.json'
        league_url = f'https://betlion-api.fsbtech.com/fsb-api-rest/bet/category/{sport_name}/league_name.json'
    elif 'betyetu' in site_name:
        password='M2b1m^ba1&ISGSJZ'
        userid='betyetu-mz'
        sport_url=f'https://betyetu-mz-api.fsbtech.com/fsb-api-rest/bet/category/{sport_name}.json'
        league_url=f'https://betyetu-mz-api.fsbtech.com/fsb-api-rest/bet/category/{sport_name}/league_name.json'

    elif 'mkekabet' in site_name:
        password = 'M2b1m^ba1&ISGSJZ'
        userid = 'betyetu-mz'
        sport_url = f'https://betyetu-mz-api.fsbtech.com/fsb-api-rest/bet/category/{sport_name}.json'
        league_url = f'https://betyetu-mz-api.fsbtech.com/fsb-api-rest/bet/category/{sport_name}/league_name.json'

    elif 'playabet' in site_name:
        password='ZMGHqkSq8muhNnHY'
        userid='playabetapi'
        sport_url=f'https://playabet-api.fsbtech.com/fsb-api-rest/bet/category/{sport_name}.json'
        league_url=f'https://playabet-api.fsbtech.com/fsb-api-rest/bet/category/{sport_name}/league_name.json'

    elif 'parimatch' in site_name:
        password = 'ZMGHqkSq8muhNnHY'
        userid = 'playabetapi'
        sport_url = f'https://playabet-api.fsbtech.com/fsb-api-rest/bet/category/{sport_name}.json'
        league_url = f'https://playabet-api.fsbtech.com/fsb-api-rest/bet/category/{sport_name}/league_name.json'

    return [sport_url,userid,password,league_url]






def get_league_matches(url,userid,password,num):
    count =0
    try:
        json_data = requests.get(url, auth=HTTPBasicAuth(userid, password)).json()
        a1 = json_data['response']['category'][0]['subcat'][0]['event']
        for event in a1:
            a2 = int(str(event['scheduledStart'])[:-3])
            if times_list[num] < a2 and times_list[num+1] > a2:
                count += 1
    except:
        pass
    return count



def get_league_names(url,userid,password,league_url):
    leagues_names = []
    json_data1 = requests.get(url,auth=HTTPBasicAuth(userid,password)).json()
    a1 = json_data1['response']['category'][0]['subcat']
    for league in a1:
        league_name = league_url.replace('league_name',league['ref'])
        leagues_names.append(league_name)
    return leagues_names


def get_count_per_sport(site_name,sport_name):
    get_urls_details = create_urls(site_name,sport_name)
    league_names = get_league_names(get_urls_details[0], get_urls_details[1], get_urls_details[2], get_urls_details[3])
    matches_count = []
    for i in range(3):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results=[executor.submit(get_league_matches,league_url,get_urls_details[1],get_urls_details[2],i) for league_url in league_names]
            d=[]
            for f in concurrent.futures.as_completed(results):
                d.append(f.result())
        total_count = sum(d)
        matches_count.append(total_count)
    return [site_name,sport_name,matches_count]


def get_data():
    list_of_matches = []
    total_data = []
    for site_name in sites_list:
        print(site_name)
        all_sports_list = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results=[executor.submit(get_count_per_sport,site_name,sport_name) for sport_name in sports_list]
            d=[]
            for f in concurrent.futures.as_completed(results):
                all_sports_list.append(f.result())
        # for sport_name in sports_list:
        #     get_count = get_count_per_sport(site_name,sport_name)
        #     all_sports_list.append(get_count)
        list_of_matches.append(all_sports_list)
        a1 = [x[2] for x in all_sports_list]
        a3=[]
        for i in range(len(all_sports_list[0][2])):
            a4 = sum([x[i] for x in a1])
            a3.append(a4)
        total_data.append([site_name,a3])

    return [list_of_matches,total_data]

