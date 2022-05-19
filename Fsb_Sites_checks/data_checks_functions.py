import datetime
import time
from Fsb_Sites_checks.Feed_checks import live_matches_all_event_ids




def click_home_page(driver):
    home_page_logo_tag = driver.find_element_by_class_name("BLM-mainHeader-logo")
    home_page_logo_a_tag = home_page_logo_tag.find_element_by_tag_name('a')
    home_page_logo_a_tag.click()
    time.sleep(5)


def duplicate_odds(match_box_element):
    sms_code = match_box_element.find_element_by_class_name('BLM-match__smsCode')
    odds_list_elements = match_box_element.find_elements_by_class_name('BLM-btnOddsGroup')
    odds_list = []
    message = []
    if len(odds_list_elements) >= 1:
        for i in odds_list_elements:
            b = i.find_elements_by_tag_name('li')
            for j in b:
                c = j.find_element_by_tag_name('button')
                odds_list.append(c.get_attribute('id'))
    # numberof_duplicate_odds_count = 0
    for i in range(len(odds_list)):
        count = 0
        for j in odds_list:
            if odds_list[i] == j:
                count += 1
        if count >= 2:
            event_id = particular_eventid(match_box_element)
            sms_code = sms_code.text
            return [f' duplicate odds at {sms_code}, {event_id}']
    return message


def particular_eventid(event_tag):
    match_tag = event_tag.find_element_by_class_name('BLM-matchDetails')
    event_onclick_tag = match_tag.get_attribute('onclick')
    total_event_details = event_onclick_tag.replace(f'getEventCode(', '')
    c = total_event_details.replace(')', '')
    get_id = []
    e = ''
    for i in c:
        e += i
        if i == ',':
            get_id.append(e)
            e = ''
        else:
            pass
    id = get_id[1][:len(get_id[1]) - 1]
    return id


def get_all_live_matches_ids(driver):
    matches_class = driver.find_elements_by_class_name('BLM-matchDetails')
    match_ids = []
    for match in matches_class:
        onclick_tag = match.get_attribute('onclick')
        value = onclick_tag.replace(f'getEventCode(', '')
        value = value.replace(')', '')
        get_id = []
        id_value = ''
        for i in value:
            id_value += i
            if i == ',':
                get_id.append(id_value)
                id_value = ''
            else:
                pass
        id = get_id[1][:len(get_id[1]) - 1]
        match_ids.append(int(id))
    return match_ids


def odds_active_or_not(driver,site_name):
    matches_elements = driver.find_elements_by_class_name('BLM-matchBox')
    # message = 'There are no matches'
    # odds_active = False
    message = []
    messages = []
    duplicate_odds_list = []
    for i in matches_elements:
        duplicate_odd = duplicate_odds(i)
        if len(duplicate_odd) > 0:
            duplicate_odds_list.append(duplicate_odd)
        else:
            pass
        sms_code_tag = i.find_element_by_class_name('BLM-match__smsCode')
        b_tag = sms_code_tag.find_element_by_tag_name('b')
        d = i.find_element_by_class_name('BLM-btnOddsGroup')
        e = d.find_elements_by_tag_name('li')
        # odds_active = True
        for j in e:
            # nam1 = j.find_element_by_tag_name('button')
            if str(j.text) == '-':
                # odds_active = False
                event_id = particular_eventid(i)
                message.append(event_id)
                # log_file('fsb_logs', '---Please check odds missing--------')
                # log_file('fsb_logs',site_name+'====' + str(c.text))
                break
    if len(message) == 0:
        pass
    else:
        messages.append('Odds not active at')
        messages.append(message)
    if len(duplicate_odds_list) >= 1:
        messages.append(duplicate_odds_list)
    return messages


def check_date_time_past_data_or_not(driver, site_name):
    a = driver.find_elements_by_class_name('BLM-matchBox')
    past_data_matches = []
    if len(a) >= 1:
        for i in a:
            sms_code_tag = i.find_element_by_class_name('BLM-match__smsCode')
            sms_code = sms_code_tag.find_element_by_tag_name('b')
            sms_code = sms_code.text
            b = i.find_element_by_class_name('BLM-match__kickOff')
            date_time = b.get_attribute('data-datetime')
            datetimeobj = datetime.datetime.strptime(date_time, "%m/%d/%Y %H:%M:%S")
            match_timestamp = datetime.datetime.timestamp(datetimeobj)
            current_time = (time.time()) - (330 * 60)
            if match_timestamp < current_time:
                past_data_matches.append(
                    f'Past data appeared at Highlights in  {site_name}: ' + sms_code)
    return past_data_matches


def live_now_data_check(driver, site_name):
    count_list = []
    messages = []
    duplicate_events = []
    a_1 = []
    try:
        all_sports_list = driver.find_element_by_class_name('BLM-categoryListCollection')
        al_sports_div_tag = all_sports_list.find_elements_by_tag_name('div')
        for sport_div_tag in al_sports_div_tag:
            class_name = sport_div_tag.get_attribute('class')
            if 'BLM-categoryListCollectionItem' in class_name:
                sport_div_tag.click()
                time.sleep(5)
                odds_active = odds_active_or_not(driver,site_name)
                if len(odds_active) > 0:
                    a_1.append(odds_active)
                sport_name = sport_div_tag.find_element_by_class_name('BLM-txtWrapper')
                sport_name = sport_name.text
                live_match_ids = get_all_live_matches_ids(driver)
                duplicate_events = []
                all_unique_events = []
                for id in live_match_ids:
                    if id in all_unique_events:
                        duplicate_events.append(id)
                    else:
                        all_unique_events.append(id)
                live_count = sport_div_tag.find_element_by_id(f'Span' + sport_name.lower())
                sport_matches_count = int(live_count.text)
                all_matches_count = driver.find_elements_by_class_name('BLM-match__smsCode')
                # match_boxes = driver.find_elements_by_class_name('BLM-matchBox')
                all_matches_count = len(all_matches_count)
                if sport_matches_count != all_matches_count:
                    # notification(f'matches count not equal for {sport_name}')
                    count_list.append(f'matches count not equal for {sport_name}')
                else:
                    pass
                if sport_name == 'Football':
                    sport_name = 'Soccer'
                if ' ' in sport_name:
                    sport_name = sport_name.replace(' ', '_')
                sport_name1 = sport_name.upper()
                live_matches_site_ids = get_all_live_matches_ids(driver)
                feed_live_matches_ids = live_matches_all_event_ids(site_name, sport_name1, '')
                missing_matches = []
                feed_match_ids = []
                for id in feed_live_matches_ids:
                    feed_match_ids.append(id[0])
                for i in range(len(feed_live_matches_ids)):
                    if feed_live_matches_ids[i][0] not in live_matches_site_ids:
                        current_time = time.time()
                        match_kickoff = str(feed_live_matches_ids[i][1])
                        get_exact_time = len(match_kickoff)
                        get_exact_time = int(match_kickoff[:get_exact_time - 3])
                        diff_time = (current_time - get_exact_time) // 60
                        if diff_time > 60 * 24:
                            pass
                        else:
                            missing_matches.append('missing: ' + str(feed_live_matches_ids[i][0]) +
                                                   '(' + str(diff_time) + ')')
                site_live_past_data = []
                for id in live_matches_site_ids:
                    if id in feed_match_ids:
                        pass
                    else:
                        site_live_past_data.append('past match ' + str(id))
                if len(missing_matches) >= 1:
                    messages.append([sport_name1])
                    messages.append(missing_matches)
                if len(site_live_past_data) >= 1:
                    messages.append(site_live_past_data)
        print('duplicate events ', duplicate_events)
    except Exception as error:
        print(error)
        print('Error at live count')
    if len(duplicate_events) > 0:
        messages.append(['Duplicate events: ', duplicate_events])
    messages.append(a_1)
    return [count_list, messages]
