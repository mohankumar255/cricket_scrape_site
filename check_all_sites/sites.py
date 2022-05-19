import selenium
import time,json
from main import send_mail

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
    #  except:
    #
    #      return [message,   False]


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


def disable_footer_notification(driver):
    try:
        close_button_id_tag = driver.find_element_by_id('dengage-push-perm-banner')
        close_button_class_tag = close_button_id_tag.find_element_by_class_name(
            'dn-banner-deny-btn')
        close_button_class_tag.click()
        time.sleep(2)
    except Exception as error:
        print(error)
        pass


def disbale_header_notification(driver):
    try:
        # notification close button class tag
        colse_btn_class_tag = driver.find_element_by_class_name("dn-slide-deny-btn")
        colse_btn_class_tag.click()
        # message = 'disabled header notification'
        time.sleep(5)
    except Exception as error:
        print(error)
        pass


from selenium import webdriver
def run(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)
    disbale_header_notification(driver)
    time.sleep(3)
    login(driver,900123123,'0000')
#run('https://mobile.betlion.ke/')


