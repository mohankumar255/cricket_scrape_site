import time
from check_all_sites.api_data import live_now_api , today_feed
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#
# driver = webdriver.Chrome()
# driver.maximize_window()
# driver.get('https://10bet.com.gh')
# time.sleep(5)




def sporst_list(driver):
    live_match_button = driver.find_element_by_id('livenow')
    a_tag = live_match_button.find_element_by_tag_name('a')
    a_tag.click()
    sports_list_buttons = driver.find_elements_by_class_name('SB-sportCategoryListItem-container')
    return len(sports_list_buttons)


def sports_page_data_checks(driver, count):
    sports_list_buttons = driver.find_elements_by_class_name('SB-sportCategoryListItem-container')
    i = sports_list_buttons[count]
    i.click()
    time.sleep(5)
    try:
        sport_id_tag = i.find_element_by_class_name('SB-txtWrapper')
        sport_id = sport_id_tag.get_attribute('id')
        sport_id = int(sport_id)
        site_total_matches = driver.find_elements_by_class_name('SB-matchDetails')
        site_total_matches = len(site_total_matches)
    except Exception as error:
        print(error)
        pass


def select_league_in_today_tab(driver):
    a1 = driver.find_element_by_id('ddlLeagues')
    a2 = a1.find_elements_by_tag_name('option')
    for i in a2:
        i.click()
        time.sleep(3)


def live_sports_clicks(driver, count ,is_live):
    sports_list_buttons = driver.find_elements_by_class_name('SB-sportCategoryListItem-container')
    i = sports_list_buttons[count]
    try:
        i.click()
    except:
        pass
    time.sleep(5)
    if True:
        sport_id_tag = i.find_element_by_class_name('SB-txtWrapper')
        sport_id = sport_id_tag.get_attribute('id')
        sport_id = int(sport_id)
        site_total_matches = driver.find_elements_by_class_name('SB-matchDetails')
        site_total_matches = len(site_total_matches)
        match_count = live_now_api(sport_id)
        feed_event_ids = live_now_api(sport_id)
        sport_name = i.text
        if match_count[0] == site_total_matches:
            pass
        else:
            sport_name = i.text
            print(f'matches missing in {i.text}')
        ids = []
        if not is_live:
            league_dropdown = driver.find_element_by_id('ddlLeagues')
            option_tags = league_dropdown.find_elements_by_tag_name('option')
            count = 0
            for option in option_tags:
                if count>0:
                    try:
                        option.click()
                        time.sleep(3)
                        event_ids = driver.find_elements_by_class_name('SB-matchBox ')
                        for event_id in event_ids:
                            id = event_id.get_attribute('id')
                            if 'highlightEvent_' in id:
                                id = id.replace('highlightEvent_', '')
                                ids.append(id)
                    except:
                        pass
                count += 1
        else:
            event_ids = driver.find_elements_by_class_name('SB-matchBox ')
            for event_id in event_ids:
                id = event_id.get_attribute('id')
                if 'highlightEvent_' in id:
                    id = id.replace('highlightEvent_', '')
                    ids.append(id)
    return [sport_id, sport_name, ids]


def get_values(site_details,is_live):
    sport_name = site_details[1]
    sport_id = site_details[0]
    site_ids = site_details[2]
    time.sleep(3)
    if is_live:

        feed_event_ids = live_now_api(sport_id)
    else:
        feed_event_ids = today_feed(sport_id)
    missing_ids = []
    past_data = []
    for id in feed_event_ids[1]:
        if id in site_ids:
            pass
        else:
            missing_ids.append(str(id))

    events = []
    duplicate_events = []
    for id in site_ids:
        if id in events:
            duplicate_events.append(id)
        else:
            events.append(id)
    for id in site_ids:
        if id not in feed_event_ids[1]:
            past_data.append('past match:' + str(id))
    return [sport_id, sport_name, f'missing matches : {len(missing_ids)} ' + str(missing_ids), past_data ,[ 'Duplicate Events', duplicate_events]]


def live_matches_data_checks(driver , is_live):
    if is_live:
        live_match_button = driver.find_element_by_id('livenow')
        a_tag = live_match_button.find_element_by_tag_name('a')
        a_tag.click()
        time.sleep(5)
    sports_list_buttons = driver.find_elements_by_class_name('SB-sportCategoryListItem-container')
    return len(sports_list_buttons)


def get_odds_data(driver,count):
    sports_list_buttons = driver.find_elements_by_class_name('SB-sportCategoryListItem-container')
    i = sports_list_buttons[count]
    i.click()
    time.sleep(5)
    try:
        sport_id_tag = i.find_element_by_class_name('SB-txtWrapper')
        sport_id = sport_id_tag.get_attribute('id')
        sport_id = int(sport_id)
        site_total_matches = driver.find_elements_by_class_name('SB-matchDetails')
        site_total_matches = len(site_total_matches)
    except Exception as error:
        print(error)
        pass




def check_all_sports_data(driver,is_live):
    if is_live:
        count = live_matches_data_checks(driver,is_live)
        add_data = []
        for i in range((count)):
            time.sleep(4)
            try:
                data1 = live_sports_clicks(driver, i,is_live)
                add_data += get_values(data1, is_live)
            except:
                pass
            break

        return [add_data,False]
    else:
        add_data = []
        count = live_matches_data_checks(driver,is_live)
        for i in range(count):
            time.sleep(4)
            try:
                data1 = live_sports_clicks(driver, i,is_live)
                add_data += get_values(data1, is_live)
            except:
                pass
            break

        return [add_data, False]

#print(check_all_sports_data(driver,False))