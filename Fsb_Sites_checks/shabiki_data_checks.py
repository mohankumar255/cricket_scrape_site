import time
import requests ,json
from selenium import webdriver

import threading,concurrent.futures


#
# url ='https://shabiki.com/'
# driver= webdriver.Chrome()
# driver.get(url)
# time.sleep(3)

def all_league_names(sport_name):
    try:
        sport_name = sport_name.upper()
        print(sport_name)
        api_url =f'https://shab-ke-api.fsbtech.com/fsb-api-rest/bet/category/{sport_name}.json'
        api_data = requests.get(api_url)
        data = api_data.json()
        all_leagues = []
        event_ids = data['response']['category'][0]['subcat']
        for league_name in event_ids:
            name = league_name['ref']
            all_leagues.append(name)
    except:
        all_leagues= []
    return all_leagues

def league_data(sport_name,league_name):

    try:
        api_url = f'https://shab-ke-api.fsbtech.com/fsb-api-rest/bet/category/{sport_name}/{league_name}.json'
        api_data = requests.get(api_url)
        data = api_data.json()
        response_code = api_data.status_code
        events = []
        event_ids = data['response']['category'][0]['subcat'][0]['event']
        for id in event_ids:
            if id['state'] == 'IN_PLAY':
                if id['virtual']:
                    pass
                elif id['displayed']:
                    events.append([id['id'], id['scheduledStart']])
                else:
                    pass
    except:
        events=[]
    return events


def duplicate_odds(driver):
    cursor_down = 0
    cursor_up = 0
    count = 0
    match_details = driver.find_elements_by_class_name('SB-matchDetails-container')
    duplicate_odds_list = []
    for match in match_details:
        event_id = match.get_attribute('attr-matchid')
        odds_group = match.find_element_by_class_name('SB-btnOddsGroup')
        is_odd_clicked = False
        buttons = odds_group.find_elements_by_tag_name('button')
        odds_list = []
        for button in buttons:
            odds_list.append(button.get_attribute('id'))
        a1 = []
        for odd in odds_list:
            if odd not in a1:
                a1.append(odd)
            else:
                duplicate_odds_list.append(event_id)
                break
    if len(duplicate_odds_list)>0:
        return ['Duplicate odds list :',duplicate_odds_list]



def sports_data(sport_name):
    a2 = time.time()
    all_league_names1 = all_league_names(sport_name)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results=[executor.submit(league_data,sport_name,all_league_names1[i]) for i in range(len(all_league_names1))]
        event_ids=[]
        for f in concurrent.futures.as_completed(results):
            if len(f.result()) > 0:
                for event_id in f.result():
                    event_ids.append(event_id)
    print(time.time()-a2)
    return event_ids

#print(a1('SOCCER'))

def duplicate_events(list_parameter):
    a1 = []
    duplicate_events = []
    for event in list_parameter:
        if event not in a1:
            a1.append(event)
        else:
            duplicate_events.append(event)
    if len(duplicate_events)>0:
        return ['Duplicate events list: ',duplicate_events]




def site_data(driver,sport_number):
    get_missing_data = []
    get_past_data = []
    if True:
        sports_list = driver.find_element_by_id('sportlist-list')
        li_tags = sports_list.find_elements_by_tag_name('li')
        all_ids = []
        scroll_right = 0
        while True:
            try:
                div_tag = li_tags[sport_number].find_element_by_tag_name('div')
                sport_name = div_tag.get_attribute('id')
                div_tag.click()
                break
            except:
                print(scroll_right)
                scroll_right+=200
                driver.execute_script(f'window.scrollTo({scroll_right},0)')
            if scroll_right>=20000:
                break
        time.sleep(5)
        if sport_name.upper()=='FOOTBALL':
            sport_name = 'SOCCER'
        sport_name = sport_name.replace(' ','_')
        sport_name = sport_name.upper()
        a5 = driver.find_elements_by_class_name('SB-matchBox')


        for event_ids in a5:
            all_ids.append(int(event_ids.get_attribute('id')))
        all_api_ids = sports_data(sport_name)
        only_api_events =[]
        for event in all_api_ids:
            only_api_events.append(event[0])
        list_of_duplicate_events = duplicate_events(all_ids)
        lis_of_duplicate_odds = duplicate_odds(driver)
        missing_matches = []
        past_matches = []
        for id in all_ids:
            if id not in only_api_events:
                past_matches.append(id)
        for id in only_api_events:
            if id not in all_ids:
                missing_matches.append(id)
        a1 = missing_matches
        b = []
        for i in a1:
            a2 = check_match(i)
            if len(a2) > 0:
                b.append(i)
        if len(b)>0:
            get_missing_data.append(['Missing data',b])
        if len(past_matches)>0:
            get_past_data.append(['Past Data',past_matches])

    collect_data = []
    if lis_of_duplicate_odds:
        collect_data.append(lis_of_duplicate_odds)
    if list_of_duplicate_events:
        collect_data.append(list_of_duplicate_events)
    if len(get_past_data)>0:
        collect_data.append(get_past_data)
    if len(get_missing_data)>0:
        collect_data.append(get_missing_data)

    if len(a5) <= 0:
        collect_data.append(f'There are no live matches in {sport_name}')
    return [sport_name+' : ',collect_data]

def check_match(match_id):
    market_names =['Match Winner','Winner','Match Result']
    url = f'https://shab-ke-api.fsbtech.com/fsb-api-rest/bet/event/{match_id}.json'
    data = requests.get(url)
    json_data = data.json()
    try:
        data_1 = json_data['response']['category'][0]['subcat'][0]['event'][0]['market']
        for book in data_1:
            data_2 = book['name']
            if data_2 in market_names:
                event_id = match_id
            else:
                event_id = ''
    except:
        event_id = match_id
    return str(event_id)


def get_livenow_data(driver):
    time.sleep(3)
    clas_name = driver.find_element_by_class_name('SB-mainHeader-container')
    a_tags = driver.find_elements_by_tag_name('a')
    for i in a_tags:
        if 'Live Now' in i.text:
            i.click()
            break
    sports_list = driver.find_element_by_id('sportlist-list')
    li_tags = sports_list.find_elements_by_tag_name('li')
    count = len(li_tags)
    get_all_data = []
    for number in range(count):
        data = site_data(driver,number)
        if len(data[1])>0:
            get_all_data.append(data)
        time.sleep(2)

    return get_all_data




def heighlights_data(driver):
    get_missing_data = []
    get_past_data = []
    all_ids = []
    a5 = driver.find_elements_by_class_name('SB-matchBox')
    for event_ids in a5:
        all_ids.append(int(event_ids.get_attribute('id')))
    list_of_duplicate_events = duplicate_events(all_ids)
    lis_of_duplicate_odds = duplicate_odds(driver)
    b = []
    collect_data = []
    if lis_of_duplicate_odds:
        collect_data.append(lis_of_duplicate_odds)
    if list_of_duplicate_events:
        collect_data.append(list_of_duplicate_events)
    if len(get_past_data) > 0:
        collect_data.append(get_past_data)
    if len(get_missing_data) > 0:
        collect_data.append(get_missing_data)
    return collect_data

def click_options_in_homepage(driver):
    all_collect_data = []
    upcoming_matches = driver.find_element_by_id('splide02-list')
    list_of_matches = upcoming_matches.find_elements_by_class_name('SB-fixtureInfo')
    if len(list_of_matches)>1:
        pass
    else:
        umpcoming_matches_data = 'Matches missing for upcoming'
        all_collect_data.append(upcoming_matches)
    a1 = driver.find_element_by_class_name('SB-tabs-boxed')
    li_tags = a1.find_elements_by_tag_name('li')
    for i in li_tags:
        option_name = i.text
        i.click()
        time.sleep(2)
        data = heighlights_data(driver)
        if len(data)>0:
            all_collect_data.append(data)
    is_fine = False
    if len(all_collect_data)>0:
        pass
    else:
        is_fine =True

    return [all_collect_data,is_fine]
#print(click_options_in_homepage(driver))


#print(get_livenow_data(driver))