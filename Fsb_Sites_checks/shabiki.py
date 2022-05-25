from selenium import webdriver
import time
from Fsb_Sites_checks.shabiki_data_checks import get_livenow_data,click_options_in_homepage


def login(driver, userid, password):
    try:
        time.sleep(3)
        a1 = driver.find_element_by_class_name('SB-mainHeader-beforeLogin')
        b = a1.find_elements_by_tag_name('a')
        for i in b:
            if 'Login' in i.text:
                i.click()
                break
        time.sleep(3)
        userid_tag = driver.find_element_by_id('userMobile')
        password_tag = driver.find_element_by_id('userPass')
        userid_tag.send_keys(userid)
        password_tag.send_keys(password)
        time.sleep(2)
        login_button = driver.find_element_by_id('disableLoginButtonClick')
        login_button.click()
        time.sleep(3)
        is_login = True
        message = 'Login Success'
    except:
        is_login = False
        message  = 'Login Failed'
    return [message,is_login,'Login']

def bet_placement(driver, stake_amount, is_multibet):
    time.sleep(3)
    if True:
        clas_name = driver.find_element_by_class_name('SB-mainHeader-container')
        a_tags = driver.find_elements_by_tag_name('a')
        for i in a_tags:
            if 'Live Now' in i.text:
                i.click()
                break
        time.sleep(3)
        odds_group = driver.find_elements_by_class_name('SB-btnOddsGroup')
        cursor_down = 0
        cursor_up = 0
        count = 0
        is_odd_clicked = False
        for odds in odds_group:
            buttons = odds.find_elements_by_tag_name('button')
            for button in buttons:
                print(button.get_attribute('class'))
                if 'SB-btnOddsDisabled' in button.get_attribute('class'):
                    pass
                elif 'btn SB-btnOdds' in button.get_attribute('class'):
                    try:
                        while True:
                            print(cursor_down)
                            try:
                                button.click()
                                is_odd_clicked = True
                                count += 1
                                time.sleep(3)
                                print('clickedddd')
                                break
                            except:
                                driver.execute_script(f'window.scrollTo(0,-{cursor_down})')
                                cursor_down += 200
                            if cursor_down >= 20000:
                                break
                        if is_odd_clicked:
                            break
                    except Exception as error:
                        print(error)

            if is_multibet:
                if count >= 3:
                    break

            else:
                if is_odd_clicked:
                    break
                    # time.sleep(3)
                    # driver.execute_script(f'window.scrollTo(0,2)')
                    # cursor_up = 0
                    # status = bet_slip(driver, stake_amount)
                    # return [status, True]
        if is_odd_clicked:
            time.sleep(10)
            driver.execute_script(f'window.scrollTo(0,2)')
            cursor_up = 0
            status = bet_slip(driver, stake_amount)
            return [status, True]
        else:
            return ['Bets not selected ,there is no active add availble',False]
    # except Exception as error:
    #     print(error)
        #return ['Betplacement is Failed', False]


def bet_slip(driver, stake):
    if True:
        stake_input = driver.find_element_by_id('stakeValue')
        stake_input.clear()
        time.sleep(1)
        stake_input.send_keys(stake)
        time.sleep(2)
        bet_place_button = driver.find_element_by_id('disablePlaceBetButton')
        bet_place_button.click()
        time.sleep(4)
        #bet_slip_status = driver.find_element_by_class_name('SB-betReceipt-header')
        message = 'Betplacement success '
        is_bet_placed = True
    # except Exception as error:
    #     print(error)
    #     message = 'Betplacement is Failed'
    #     is_bet_placed = False
    return [message, is_bet_placed]


def jackpot(driver):
    clas_name = driver.find_element_by_class_name('SB-mainHeader-container')
    a_tags = driver.find_elements_by_tag_name('a')
    try:
        driver.switch_to_alert().dismiss()
    except:
        pass
    time.sleep(2)
    for i in a_tags:
        if 'Jackpot' in i.text:
            i.click()
            break
    time.sleep(5)
    driver.switch_to_frame('virtualFrame')
    jackpot_play_button = driver.find_element_by_class_name('NP-cardBanner__actions')
    button = jackpot_play_button.find_element_by_tag_name('button')
    button.click()
    time.sleep(4)
    selection_buttons = driver.find_element_by_class_name('fillterSelections')
    auto_pic_button = selection_buttons.find_element_by_tag_name('li')
    auto_pic_button.click()
    time.sleep(2)
    cursor_down = 0
    while True:
        try:
            submit_button = driver.find_element_by_id('disableplaynowbtnclick')
            submit_button.click()
            break
        except:
            driver.execute_script(f'window.scrollTo(0,-{cursor_down})')
            cursor_down += 400
        if cursor_down >= 20000:
            break
    time.sleep(3)

    cursor_up = 0
    while True:
        try:
            submit_button = driver.find_element_by_id('betslip')
            submit_button.click()
            break
        except:
            driver.execute_script(f'window.scrollTo(0,{cursor_up})')
            cursor_up += 400
        if cursor_up >= 20000:
            break
    driver.execute_script(f'window.scrollTo(0,2)')
    time.sleep(2)
    try:
        message = driver.find_element_by_class_name('NP-betReceipt-betSuccess').text
        is_jackpot_done = True
    except:
        message = 'Jackpot Failed'
        is_jackpot_done = False
    cursor_up = 0
    return [message, is_jackpot_done]


def cashout(driver):
    try:
        time.sleep(3)
        a = driver.find_element_by_id('balancePopup')
        a1 = a.find_element_by_tag_name('button')
        a1.click()
        time.sleep(3)
        a2 = driver.find_elements_by_class_name('SB-myAccountList-item')
        for i in a2:
            print(i.text)
            if 'Cashout' in i.text:
                a3 = i.find_element_by_tag_name('a')
                a3.click()
                break
        time.sleep(2)
        a4 = driver.find_element_by_class_name('SB-cashOut-container')
        button = a4.find_element_by_tag_name('button')
        button.click()
        time.sleep(2)
        a5 = driver.find_element_by_class_name('SB-betBox-btnCashout-container')
        a6 = a5.find_elements_by_tag_name('button')
        a6[1].click()
        time.sleep(2)
        message = 'Cashout Success'
        is_cashout = True
    except:
        message = 'Cashout Failed or no cashouts available'
        is_cashout = False
    return [message, is_cashout]


def withdraw(driver):
    try:
        time.sleep(3)
        a = driver.find_element_by_id('balancePopup')
        a1 = a.find_element_by_tag_name('button')
        a1.click()
        time.sleep(3)
        a2 = driver.find_elements_by_class_name('SB-myAccountList-item')
        for i in a2:
            print(i.text)
            if 'Withdraw' in i.text:
                a3 = i.find_element_by_tag_name('a')
                a3.click()
                break
        time.sleep(2)

        button = driver.find_element_by_id('disableWithdrawButtonClick')
        button.click()
        time.sleep(3)
        title = driver.find_element_by_class_name('SB-pageHeader-title').text
        if 'Success' in title:
            is_withdraw = True
        else:
            is_withdraw = False
            message = 'Withdraw Failed'
        message = driver.find_element_by_class_name('SB-msgBox-container').text

    except Exception as error:
        message = str(error)
        is_withdraw = False

    return [message, is_withdraw]


def deposite(driver):
    a = driver.find_element_by_class_name('SB-mainHeader-freeBetDeposit')
    a_tag = a.find_element_by_tag_name('a')
    a_tag.click()
    time.sleep(3)
    a2 = driver.find_element_by_class_name('SB-paymentMethod-footer')
    a3 = a2.find_element_by_tag_name('button')
    a3.click()
    time.sleep(3)
    deposite_button = driver.find_element_by_id('disableDepositButtonClick')
    deposite_button.click()
    time.sleep(3)
    error_message = driver.find_element_by_id('errorMessageDepositClass').text
    message = error_message
    if len(error_message) > 5:
        is_deposite = False
    else:
        is_deposite = True
        message = 'Deposite SUccess'
    return [message, is_deposite]


def logout(driver):
    time.sleep(5)
    try:
        a = driver.find_element_by_id('balancePopup')
        a1 = a.find_element_by_tag_name('button')
        a1.click()
        time.sleep(3)
        a1 = driver.find_element_by_class_name('SB-myAccount-container')
        buttons = a1.find_elements_by_tag_name('button')
        for i in buttons:
            if 'Logout' in i.text:
                print(i.text)
                i.click()
                time.sleep(3)
                break
        is_logout = True
        message = 'Logout done'
    except Exception as error:
        is_logout = False
        message = 'Logout Failed'
    return [message, is_logout,'Logout']


# user_id,password)
time.sleep(3)


#print(bet_placement(driver,2,False))
# time.sleep(3)
# print(cashout(driver))
# time.sleep(3)
# print(withdraw(driver))
# time.sleep(3)
# print(deposite(driver))
# time.sleep(3)
# print(logout(driver))
# jackpot(driver)

# a(driver)


def check_site(site_name,url,userid,password,stake,filters):
    print(filters)
    functions_names = []
    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()
    time.sleep(3)
    all_details = []
    all_details.append([url, True,"Site Name"])
    #bet_placement_data = bet_placement(driver, stake, False)
    time.sleep(5)
    if True:
        if 2 in filters:
            all_details.append(click_options_in_homepage(driver))
        if 3 in filters:
            all_details.append(get_livenow_data(driver))
        if 4 in filters:
            login_detials = login(driver, userid, password)
            all_details.append(login_detials)
            if login_detials[1]:
                if 9 in filters:
                    try:
                        all_details.append(withdraw(driver))
                    except:
                        all_details.append(['Withdraw Failed', False])
                if 7 in filters:
                    try:
                        all_details.append(deposite(driver))
                    except:
                        all_details.append(['Deposite Failed', False])
                if 5 in filters:
                    #bet_placement_data = bet_placement(driver, stake, False)
                    bet_placement_data = bet_placement(driver, stake, False)
                    all_details.append(bet_placement_data)
                    # try:
                    #     bet_placement_data = bet_placement(driver, stake, False)
                    #     all_details.append(bet_placement_data)
                    # except:
                    #     pass
                if 12 in filters:

                    try:
                        bet_placement_data = bet_placement(driver, stake, True)
                        all_details.append(bet_placement_data)
                    except :
                        pass
                    time.sleep(5)
                if 8 in filters:
                    all_details.append(cashout(driver))
                if 6 in filters:
                    try:
                        all_details.append(jackpot(driver))
                    except:
                        all_details.append(['Jackpot failed', False])
                if 13 in filters:
                    logout_data = logout(driver)
                    all_details.append(logout_data)
            else:
                pass
        # all_details.append([f'Error occured at {site_name}',False])
    driver.close()
    return all_details
#print(check_site([4,5,7,8,9,13]))
