import time
import datetime
from selenium import webdriver

#driver.get('https://10bet.co.tz/')
from check_all_sites.api_data import live_now_api

import smtplib
from email.message import EmailMessage

def send_mail(subject, message):
    from_add = 'mk3026201@gmail.com'
    to_add = 'kumarmohan143123@gmail.com'
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_add
    msg['To'] = to_add
    msg.set_content(message)
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(from_add, 'Nmohan@123')
    server.send_message(msg)
    server.quit()


# login(driver)


def live_matches_data_checks(driver):
    live_match_button = driver.find_element_by_id('livenow')
    a_tag = live_match_button.find_element_by_tag_name('a')
    a_tag.click()
    sports_list_buttons = driver.find_elements_by_class_name('SB-sportCategoryListItem-container')
    return len(sports_list_buttons)


def live_sports_clicks(driver, count):
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
        match_count = live_now_api(sport_id)
        feed_event_ids = live_now_api(sport_id)
        sport_name = i.text
        if match_count[0] == site_total_matches:
            pass
        else:
            sport_name = i.text
            print(f'matches missing in {i.text}')
        event_ids = driver.find_elements_by_class_name('SB-match__scoreInfo')
        ids = []
        missing_ids = []
        past_data = []
        for i in event_ids:
            id = i.get_attribute('id')
            if 'score_' in id:
                id = id.replace('score_', '')
                ids.append(id)
        for id in feed_event_ids[1]:
            if id in ids:
                pass
            else:
                missing_ids.append(str(id))
        for id in ids:
            if id not in feed_event_ids[1]:
                past_data.append('past match:' + str(id))

        if len(past_data) > 0:
            send_mail(f'Past matches in  {sport_name}')
        if len(past_data) > 0:
            send_mail(f'Past matches in {sport_name}')
        return [sport_id, sport_name, 'missing matches :' + str(missing_ids), past_data]
    except Exception as error:
        print(error)
        return [False]


def check_all_sports_data(driver):
    count = live_matches_data_checks(driver)
    for i in range(count):
        time.sleep(4)
        print(live_sports_clicks(driver, i))


def bet_placement(driver):
    live_match_button = driver.find_element_by_id('livenow')
    a_tag = live_match_button.find_element_by_tag_name('a')
    a_tag.click()
    time.sleep(3)
    y_axis = 100
    odds_buttons_group_tag = driver.find_elements_by_class_name('SB-btnOddsGroup')
    for i in odds_buttons_group_tag:
        odds_buttons = i.find_elements_by_tag_name('button')
        while True:
            driver.execute_script(f'window.scrollTo(0,{y_axis});')
            try:
                for j in odds_buttons:
                    j.click()
                    time.sleep(2)
                    break
                break
            except:
                y_axis += 200
        break
    driver.execute_script(f'window.scrollTo(0,-{y_axis});')
    stake_amount_input_tag = driver.find_element_by_id('getParlayStakeId')
    stake_amount_input_tag.send_keys(2)
    time.sleep(2)
    bet_place_button = driver.find_element_by_id('parlayPlacebetButtonActiveId')
    bet_place_button.click()
    time.sleep(8)
    click_on_betslip_page = driver.find_element_by_class_name('SB-betSlip-errorMsg')
    a_tag = click_on_betslip_page.find_element_by_tag_name('a')
    a_tag.click()
    time.sleep(3)
    bet_status_tag = driver.find_element_by_class_name('SB-myBetBox-header-right')
    bet_status = bet_status_tag.text
    return [bet_status]


# login(driver)
#check_all_sports_data(driver)


# bet_placement(driver)

