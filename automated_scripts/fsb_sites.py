from selenium import webdriver
import time
from check_all_sites.main import send_mail
from Fsb_Sites_checks.comman_use_libraries import *


def select_language(driver):
    left_side_button_click = driver.find_element_by_class_name('BLM-hamBurger-menu')
    left_side_button_click.click()
    time.sleep(5)
    dropdown_select_tag = driver.find_element_by_id('ddn_languages')
    dropdown_select_tag.click()
    time.sleep(3)
    select_option_tag = dropdown_select_tag.find_elements_by_tag_name('option')
    select_option_tag[1].click()
    time.sleep(5)


def login(driver, user_id, password):
    print(user_id, password)
    login_button_tag = driver.find_element_by_class_name('BLM-mainHeader-loginRegister')
    login_button_tag = login_button_tag.find_element_by_tag_name('a')
    login_button_tag.click()
    time.sleep(5)
    user_id_tag = driver.find_element_by_id('userMobile')
    password_id_tag = driver.find_element_by_id('userPass')
    user_id_tag.send_keys(user_id)
    password_id_tag.send_keys(password)
    login_button = driver.find_element_by_id('disableLoginButtonClick')
    login_button.click()
    time.sleep(5)
    if True:
        bln = driver.find_elements_by_id('headerUserBalanceDisplay')
        if len(bln) >= 1:
            message = 'Loged in Succesfully'
            print(message)
            return [message, True]
        else:
            error_message = driver.find_element_by_id('displayErrorMessage')
            message = error_message.find_element_by_tag_name('span')
            message = message.text
            return [message, False]



def bet_placement123(driver, url, stake_amount, is_multibet):
    a = driver.find_element_by_id('liveMatches')
    a.click()
    time.sleep(5)
    login_status = False
    bet_placement_status = False
    balance = ''
    message = ''
    active_odds_count = 0
    try:
        bln = driver.find_element_by_id('headerUserBalanceDisplay')
        amount = bln.text
        for i in amount:
            if i == '.':
                break
            else:
                try:
                    a = int(i)
                    balance += str(a)
                except Exception as error:
                    pass
        balance = int(balance)
        if balance > 30:
            bet_place_status = True
        else:
            bet_place_status = False
            message = 'Due to low balance unable to place bet'
    except Exception as error:
        print(error)
        bet_place_status = False
        # notification(f'please check {url} login')
        #  --------------
    try:

        if bet_place_status:
            sportsid_list = driver.find_elements_by_id('sportlist')
            match = driver.find_elements_by_class_name('BLM-matchBox')
            count = 0
            click_odds_count = 0
            for j in match:
                odds_values = j.find_elements_by_class_name('BLM-btnOddsGroup')
                for i in odds_values:
                    # li_value = i.find_element_by_tag_name('li')
                    odds_button_tag = j.find_element_by_tag_name('button')
                    odds_button_status = odds_button_tag.get_attribute('class')
                    if 'btn BLM-btnOdds BLM-btnOddsDisabled' in odds_button_status:
                        pass
                    else:
                        message = i.text
                        if True:
                            time.sleep(2)
                            # driver.execute_script('window.scrollTo(0,  300);')
                            # time.sleep(2)
                            active_odds_count = 1
                            value = 0
                            while True:
                                value += 100
                                try:
                                    odds_button_tag.click()
                                    click_odds_count += 1
                                    break
                                except:
                                    driver.execute_script(f'window.scrollTo(0,  {value})')
                            break
                if is_multibet:
                    if len(match) >= 4:
                        if click_odds_count == 4:
                            break
                    else:
                        pass
                else:
                    if click_odds_count >= 1:
                        break
                    # driver.execute_script('window.scrollTo(0,  -10);')
        if active_odds_count >= 1:
            betslip_message = betslip(driver, stake_amount, url, is_multibet)
            bet_placement_status = betslip_message[1]
            message = betslip_message[0]
        else:
            bet_placement_status = False
            message = 'There are No active odds for first active sports'
    except Exception as error:
        print(error)
        message = 'Error occured at Betplacement'
        bet_placement_status = False
    print(message, bet_placement_status)
    return [message, bet_placement_status]


def betslip(driver, stake_amount, url, is_multibet):
    time.sleep(5)
    bet_slip_tag = driver.find_element_by_id('BLM-betSlip-Button')
    bet_slip_tag.click()
    time.sleep(5)
    stake_tag = driver.find_element_by_id('stakeValue')
    stake_tag.clear()
    stake_tag.send_keys(stake_amount)
    bet_place_button_tag = driver.find_element_by_id('disablePlaceBetButton')
    bet_placement_status = False
    bet_place_button_tag.click()
    time.sleep(30)
    try:
        try:
            bet_status_tag = driver.find_element_by_class_name('BLM-betReceipt-betSuccess')
            bet_status = bet_status_tag.text
            message = bet_status
            close_receipt = driver.find_element_by_class_name('BLM-betReceipt-btnClose')
            driver.back()
            time.sleep(5)
            bet_placement_status = True
        except Exception as error:
            print(error)
            bet_status_tag = driver.find_element_by_class_name('BLM-betReceipt-betSuccessMsg')
            bet_status = bet_status_tag.text
            message = bet_status
            bet_placement_status = True
            driver.back()
            time.sleep(5)
    except Exception as error:
        print(error)
        error_message = driver.find_element_by_id('placeBetErrorMessageDisplay')
        span_tag = error_message.find_element_by_tag_name('span')
        span_tag_message = error_message.text
        message = span_tag_message
        print(span_tag_message)
        close_receipt_button = driver.find_element_by_class_name('BLM-betSlip-closeButton')
        # close_receipt_button = close_receipt.find_element_by_tag_name('button')
        driver.back()
        time.sleep(5)
        bet_placement_status = False

    print('----------------------------------')
    return [message, bet_placement_status]


def my_account_tab(driver):
    account_tab_status = False
    try:
        menu_click = driver.find_element_by_class_name('BLM-hamBurger-menu')
        menu_click.click()
        time.sleep(3)
        menu_items = driver.find_element_by_class_name('sidemenu-tablist')
        a_tags = menu_items.find_elements_by_tag_name('a')
        for i in a_tags:
            a = i.get_attribute('href')
            message = (a)
            if 'BLM-sideMenu-myAccount' in a:
                i.click()
                time.sleep(5)
                break
        account_tab_status = True
    except Exception as error:
        message = (error)
        my_account_tab(driver)
    return account_tab_status


def logout(driver):
    logout_status = False
    value = 0
    while True:
        try:
            value += 100
            driver.execute_script(f'window.scrollTo(0,  {value});')
            logout_tag = driver.find_element_by_class_name('BLM-logout-container')
            logout_button = logout_tag.find_element_by_tag_name('button')
            logout_button.click()
            time.sleep(5)
            login_button_tag = driver.find_element_by_class_name('BLM-mainHeader-loginRegister')
            logout_status = True
            if 'Login' in login_button_tag.text:
                message = ('logout done')
            break
        except Exception as error:
            if value == 10000:
                break
            print(error)
            logout_status = False
            message = ('logout not done ,  please check it')
    return [message, logout_status]



def site_checks(site_name, url, user_id, password, stake_amount):
    all_checks_status = []
    driver = webdriver.Chrome(r'C:\Users\User 101\Desktop\automation projects\cricket_scrape_site\chromedriver.exe')
    driver.get(url)
    driver.maximize_window()
    time.sleep(5)
    if 'betyetu' in url:
        select_language(driver)
    disbale_header_notification(driver)

    try:
        login_status = login(driver,user_id,password)
        if login_status[1]:
            hours = time.strftime('%H')
            minutes = time.strftime('%M')

            bet_status = ['Betfailed',False]
            if int(hours)%6==0:

                if int(minutes)>3 and int(minutes)<=10:
                    disable_footer_notification(driver)
                    for i in range(3):
                        bet_status = bet_placement123(driver,url,stake_amount,False)
                        if bet_status[1]:
                            break
                        else:
                            pass
                    if bet_status[1]:
                        pass
                    else:
                        send_mail(f'Betfailed in {site_name}',bet_status[0])
                    time.sleep(3)
                    for i in range(3):
                        bet_status = bet_placement123(driver, url, stake_amount, True)
                        if bet_status[1]:
                            break
                        else:
                            pass
                    if bet_status[1]:
                        pass
                    else:
                        send_mail(f'Betfailed in {site_name}', bet_status[0])
            time.sleep(3)
            my_account_tab(driver)
            disable_footer_notification(driver)
            time.sleep(3)
            logout_status = logout(driver)
            if logout_status[1]:
                pass
            else:
                send_mail(f'Logout Failed {site_name}',logout_status[0])
        else:
            send_mail(f'Login Failed {site_name}',login_status[0])
    except Exception as error:
        send_mail(f"{site_name} Site is not loading please check it ",str(error))
    driver.close()


from Fsb_Sites_checks.fsb_db import *
import threading

all_menus_list = get_all_menus()
all_submenus_details = get_all_submenus_list()

mobile_sites = []
opera_sites = []
for site in all_submenus_details:
    if '//m.' in site[1]:
        opera_sites.append(site)
    else:
        mobile_sites.append(site)
def run_fsb_sites():
    list1 = []
    for i in range(len(mobile_sites)):
        a1 = threading.Thread(target=site_checks, args=(mobile_sites[i][0],mobile_sites[i][1],mobile_sites[i][3],mobile_sites[i][4],mobile_sites[2]))
        list1.append(a1)
    for j in list1:
        j.start()
    for k in list1:
        k.join()

    time.sleep(10)
    list1 = []
    for i in range(len(opera_sites)):
        a1 = threading.Thread(target=site_checks, args=(
        opera_sites[i][0], opera_sites[i][1], opera_sites[i][3], opera_sites[i][4],opera_sites[2]))
        list1.append(a1)
    for j in list1:
        j.start()
    for k in list1:
        k.join()
