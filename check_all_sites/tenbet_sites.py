from selenium import webdriver
from check_all_sites.main import send_mail
import time
from check_all_sites.tenbet_datachecks import check_all_sports_data

url1 = 'https://m.10bet.co.tz/login?overrideregion=true'
url2 = 'https://10bet.com.gh/login?overrideregion=true'
url3 = 'https://10bet.co.zm/login?overrideregion=true'
url4 = 'https://10betdrc.com/login?overrideregion=true'

userid_1 = 765765765
password_1 = 1234

userid_2 = 245245245
password_2 = 1234

userid_3 = 962962962
password_3 = 1234

userid_4 = 840840840
password_4 = 1234


def login1(driver, url, user_id, password):
    print(url,user_id,password)
    try:
        time.sleep(5)
        userid_input = driver.find_element_by_id('regMobile')
        password_input = driver.find_element_by_id('regPass')
        userid_input.send_keys(user_id)
        password_input.send_keys(password)
        time.sleep(1)
        a1 = driver.find_elements_by_tag_name('button')
        for i in a1:
            print(i.get_attribute('class'))
        count = 0
        for i in a1:
            if '//m' in url:
                if 'btn SB-btnSecondary active SB-btnMedium' == i.get_attribute('class'):
                    print(i.get_attribute('class'))
                    time.sleep(1)
                    print('click')
                    i.click()
                    break

            else:
                if 'btn SB-btnSecondary active SB-btnLarge' in i.get_attribute('class'):
                    time.sleep(1)
                    print('click')
                    i.click()
                    break
        time.sleep(3)
        is_login = False
        print('--------------------------------')
        for i in range(8):
            print(url)
            try:
                mainbalance = driver.find_element_by_id('mainHeaderBalance')
                is_login = True
                message = 'Logeed in successfully'
                break
            except Exception as error:
                print(error)
                driver.refresh()
                time.sleep(2)
                userid_input = driver.find_element_by_id('regMobile')
                password_input = driver.find_element_by_id('regPass')
                userid_input.send_keys(user_id)
                password_input.send_keys(password)
                time.sleep(1)
                a1 = driver.find_elements_by_tag_name('button')
                count = 0
                for i in a1:
                    if '//m.' in url:
                        if 'btn SB-btnSecondary active SB-btnMedium' == i.get_attribute('class'):
                            print(i.get_attribute('class'))

                            time.sleep(1)
                            print('click')
                            i.click()
                            break
                    else:
                        if 'btn SB-btnSecondary active SB-btnLarge' in i.get_attribute('class'):
                            time.sleep(1)
                            print('click')
                            i.click()
                            time.sleep(3)
                        break
                is_login = False
                message = 'Login failed please check it'
    except Exception as error:
        print(error)
        is_login = False
        message = 'Login failed please check it'
    return [message, is_login]



def login(driver, url, user_id, password):
    print(user_id,password)
    try:
        time.sleep(10)
        userid_input = driver.find_element_by_id('userMobileNo')
        password_input = driver.find_element_by_id('userPassword')
        userid_input.send_keys(user_id)
        password_input.send_keys(password)
        time.sleep(5)
        login_box = driver.find_element_by_id('disableLoginButtonClick')
        login_box.click()
        time.sleep(3)
        error_message = driver.find_element_by_id('loginErrorMessage')
        message = error_message.text
        print('--==============', message)
        if len(message) > 0:
            message = message
        else:
            message = 'Login Success'
        driver.refresh()
        time.sleep(5)
        is_login = False
        print('--------------------------------')
        try:
            mainbalance = driver.find_element_by_id('mainHeaderBalance')
            is_login = True
        except Exception as error:
            print(error)
            is_login = False
            message = 'Login failed please check it'
        time.sleep(3)
    except Exception as error:
        is_login = False
        message = 'Login failed please check it'
    return [message, is_login]


def jackpot(driver):
    try:
        live_match_button = driver.find_element_by_id('jackpot')
        a_tag = live_match_button.find_element_by_tag_name('a')
        a_tag.click()
        is_jackpot_availble = True
    except:
        message = 'There is no jackpot available'
        is_jackpot_availble = False
    if is_jackpot_availble:
        time.sleep(10)
        driver.switch_to.frame('virtualFrame')
        time.sleep(3)
        jackpot_class = driver.find_elements_by_class_name("NP-cardBanner__actions")
        print(len(jackpot_class))
        if len(jackpot_class) > 0:
            button = jackpot_class[0].find_element_by_tag_name('button')
            button.click()
            time.sleep(3)
            filters_class_name = driver.find_element_by_class_name('fillterSelections')
            li = filters_class_name.find_element_by_tag_name('li')
            li.click()
            time.sleep(3)
            submit = driver.find_element_by_id('disableplaynowbtnclick')
            count = 0
            while True:
                try:
                    driver.execute_script(f'window.scrollTo(0,{count});')
                    submit.click()
                    time.sleep(3)
                    break
                except:
                    count += 200
                if count >= 20000:
                    break
            time.sleep(4)
            message = driver.find_element_by_class_name('NP-betReceipt-betSuccess').text
        else:
            message = 'There are no jackpots'
        count = 0
    driver.execute_script(f'window.scrollTo(0,2)')
    return [message, is_jackpot_availble]


def bet_placement1(driver, site_name, stake, is_multibet):
    try:
        live_match_button = driver.find_element_by_id('livenow')
        a_tag = live_match_button.find_element_by_tag_name('a')
        a_tag.click()
        time.sleep(3)
        y_axis = 100
        count = 0
        button_click = False
        odds_buttons_group_tag = driver.find_elements_by_class_name('SB-btnOddsGroup')
        for i in odds_buttons_group_tag:
            odds_buttons = i.find_elements_by_tag_name('button')
            print(len(odds_buttons))
            while True:
                try:
                    for j in odds_buttons:
                        j.click()
                        button_click = True
                        time.sleep(4)
                        count += 1
                        break
                    break
                except:
                    driver.execute_script(f'window.scrollTo(0,-{y_axis});')
                    y_axis += 200
            if is_multibet:
                if count > 2:
                    break
            else:
                if button_click:
                    break
        driver.execute_script(f'window.scrollTo(0,-{y_axis});')
        stake_amount_input_tag = driver.find_element_by_id('getParlayStakeId')
        stake_amount_input_tag.clear()
        time.sleep(2)
        stake_amount_input_tag.send_keys(stake)
        time.sleep(2)
        bet_place_button = driver.find_element_by_id('parlayPlacebetButtonActiveId')
        bet_place_button.click()
        time.sleep(8)
        click_on_betslip_page = driver.find_element_by_class_name('SB-betSlip-errorMsg')
        text_message = click_on_betslip_page.text
        a_tag = click_on_betslip_page.find_element_by_tag_name('a')
        a_tag.click()
        time.sleep(8)
        bet_status_tag = driver.find_element_by_class_name('SB-myBetBox-header-right')
        message = bet_status_tag.text
        is_bet = True
    except Exception as error:
        print(error)
        is_bet = False
        message = 'Bet placement is failed'
    return [message, is_bet]


def change_language(driver):
    id1 = driver.find_element_by_id('ddn_languages')
    options_tag = id1.find_elements_by_tag_name('option')
    options_tag[-1].click()
    time.sleep(3)


def withdraw(driver):
    balance_button = driver.find_element_by_class_name('SB-dropdown-btn')
    balance_button.click()
    time.sleep(15)
    a = driver.find_element_by_class_name("SB-myAccountList")
    a1 = a.find_elements_by_class_name('SB-myAccountList-item')

    a2 = a1[-4].find_element_by_class_name('SB-myAccountList-item-content')
    print(a2.text)
    a3 = a2.find_element_by_tag_name('a')
    a3.click()
    time.sleep(5)
    input_id = driver.find_element_by_id('enterWithdrawValue')
    input_id.send_keys(10)
    time.sleep(2)
    withdraw_button = driver.find_element_by_id('disableWithdrawButtonClick')
    withdraw_button.click()
    time.sleep(2)
    error_message2 = ''
    error_message = driver.find_element_by_id('errorMessageWithdrawAmountClass').text
    try:
        error_message2 = driver.find_element_by_class_name('BLM-msgBox-container').text
    except:
        pass

    if len(error_message) > 2:
        message = error_message
        withdraw_done = False
    elif len(error_message2) > 2:
        message = error_message2
        withdraw_done = False
    else:
        message = 'WithDraw success'
        withdraw_done = True
    home_page_logo = driver.find_element_by_class_name('SB-mainHeader-logo')
    home_page_logo.click()
    time.sleep(5)
    return [message, withdraw_done]


def logout(driver):
    try:
        balance_button = driver.find_element_by_class_name('SB-dropdown-btn')
        balance_button.click()
        time.sleep(4)
        a = driver.find_element_by_class_name("SB-myAccountList")
        a1 = a.find_elements_by_class_name('SB-myAccountList-item')
        a2 = a1[-1].find_element_by_class_name('SB-myAccountList-item-content')
        a3 = a2.find_element_by_tag_name('a')
        for i in range(5):
            try:
                a3.click()
                break
            except Exception as error:
                print(error)
        time.sleep(5)
        is_logout = True
        logout_message = 'Logout Done'
    except Exception as error:
        print(error)
        is_logout = False
        logout_message = 'Logout failed'
    return [logout_message, is_logout]


list1 = [[], ['TZ',url1, userid_1, password_1, 100, ], ['GH',url2,  5,userid_2, password_2],
         ['ZM',url3, 5, userid_3, password_1], ['CH',url4, 5,userid_4, password_4]]


def opera_cashouts(driver):
    # home_page_logo = driver.find_element_by_class_name('SB-mainHeader-logo')
    # home_page_logo.click()
    # time.sleep(5)
    driver.find_element_by_id('mybets').click()
    time.sleep(5)
    number_of_open_bets = driver.find_elements_by_class_name('SB-cashOut-container')
    if len(number_of_open_bets) > 0:
        y_axis = 0
        while True:
            try:
                driver.execute_script(f'window.scrollTo(0,-{y_axis});')
                number_of_open_bets[0].click()
                break
            except:
                y_axis+=500
            if y_axis>=20000:
                break
            time.sleep(5)
        class1 = driver.find_element_by_class_name('SB-cashOut-btn-container')
        button = class1.find_element_by_tag_name('button')
        y_axis = 0
        while True:
            driver.execute_script(f'window.scrollTo(0,-{y_axis});')
            try:
                button.click()
                break
            except:
                y_axis += 200
            if y_axis >= 20000:
                break
        time.sleep(3)
        try:
            confirm_button = driver.find_element_by_class_name('SB-cashOut-btn-container')
            btn = confirm_button.find_element_by_tag_name('button')
            btn.click()
            time.sleep(4)
        except:
            pass

        driver.refresh()
        time.sleep(3)
        after_cashout_number_of_open_bets = driver.find_elements_by_class_name('SB-cashOut-container')
        if len(after_cashout_number_of_open_bets)!=number_of_open_bets:
            is_cashout = True
            message = 'Cashout Success'
        else:
            is_cashout = False
            message = 'Cashout Failed'
    else:
        is_cashout = True
        message = 'There are no cashouts'

    # except:
    # is_cashout = False
    # message = 'Cashout Failed'
    return [message, is_cashout]


def deposite(driver):
    driver_class_name = driver.find_element_by_class_name('SB-mainHeader-freeBetDeposit')
    a_tag = driver_class_name.find_element_by_tag_name('button')
    print(a_tag.text)
    for i in range(5):
        try:
            a_tag.click()
            time.sleep(2)
            break
        except:
            pass
    time.sleep(5)
    online_id = driver.find_element_by_id('Online')
    for i in range(5):
        try:
            online_id.click()
            time.sleep(2)
            break
        except:
            pass
    time.sleep(5)
    a1 = driver.find_element_by_class_name('SB-radioBoxGroup')
    b = a1.find_element_by_tag_name('input')
    driver.execute_script('arguments[0].click()', b)
    time.sleep(3)
    # operator_id = driver.find_element_by_id('depositSelection1')
    # time.sleep(2)
    # operator_id.click()
    # time.sleep(2)
    # amount_input = driver.find_element_by_id('enterDepositValue')
    # amount_input.clear()
    # time.sleep(2)
    # amount_input.send_keys(5)
    a1 = driver.find_element_by_id('depositAmount1')
    a1.click()
    time.sleep(2)

    deposite_button = driver.find_element_by_id('disableDepositButtonClick')
    deposite_button.click()
    time.sleep(5)
    text1 = driver.find_element_by_class_name('SB-pageHeader-title').text
    is_deposite = True
    home_page_logo = driver.find_element_by_class_name('SB-mainHeader-logo')
    home_page_logo.click()
    time.sleep(5)
    return [text1, is_deposite]


def cashout(driver):
    try:
        home_page_logo = driver.find_element_by_class_name('SB-mainHeader-logo')
        home_page_logo.click()
        time.sleep(5)
        a1 = driver.find_element_by_id('getMyBetsCountDisplay').text
        number_of_open_bets = int(a1)
        if number_of_open_bets > 0:
            openbets_click = driver.find_element_by_id('MyBetsTabId').click()
            time.sleep(5)
            class1 = driver.find_element_by_class_name('SB-myBets-cashout-container')
            button = class1.find_element_by_tag_name('button')
            y_axis = 0
            while True:
                driver.execute_script(f'window.scrollTo(0,-{y_axis});')
                try:
                    button.click()
                    break
                except:
                    y_axis += 200
                if y_axis >= 20000:
                    break
            time.sleep(3)
            confirm_button = driver.find_element_by_class_name('SB-cashOut-btn-container')
            btn = confirm_button.find_element_by_tag_name('button')
            btn.click()
            time.sleep(4)
            is_cashout = True
            message = 'Cashout Success'

        else:
            is_cashout = True
            message = 'There are no cashouts'
    except:
        is_cashout = False
        message = 'Cashout Failed'
    return [message, is_cashout]

def opera_site_betplacement(driver,stake,is_multibet):
    if True:
        live_match_button = driver.find_element_by_id('livenow')
        live_match_button.click()
        #a_tag = live_match_button.find_element_by_tag_name('a')
        #a_tag.click()
        time.sleep(3)
        y_axis = 100
        count = 0
        button_click = False
        odds_buttons_group_tag = driver.find_elements_by_class_name('SB-btnOddsGroup')
        for i in odds_buttons_group_tag:
            odds_buttons = i.find_elements_by_tag_name('button')
            print(len(odds_buttons))
            while True:
                try:
                    for j in odds_buttons:
                        j.click()
                        button_click = True
                        time.sleep(4)
                        count += 1
                        break
                    break
                except Exception as error:
                    print(error)
                    driver.execute_script(f'window.scrollTo(0,-{y_axis});')
                    y_axis += 200
            if is_multibet:
                if count > 2:
                    break
            else:
                if button_click:
                    break
        driver.execute_script(f'window.scrollTo(0,-{y_axis});')
        time.sleep(3)
        driver.find_element_by_class_name('SB-btn-container').click()
        time.sleep(4)
        stake_amount_input_tag = driver.find_element_by_id('getParlayStakeId')
        stake_amount_input_tag.clear()
        time.sleep(2)
        stake_amount_input_tag.send_keys(stake)
        time.sleep(2)
        bet_place_button = driver.find_element_by_id('parlayPlacebetButtonActiveId')
        bet_place_button.click()
        time.sleep(8)
        click_on_betslip_page = driver.find_element_by_class_name('SB-betSlip-errorMsg')
        text_message = click_on_betslip_page.text
        a_tag = click_on_betslip_page.find_element_by_tag_name('a')
        a_tag.click()
        time.sleep(8)
        bet_status_tag = driver.find_element_by_class_name('SB-myBetBox-header-right')
        message = bet_status_tag.text
        is_bet = True
    # except Exception as error:
    #     is_bet = False
    #     message = 'Bet placement is failed'
    return [message, is_bet]


def check_site(site_name,url, stake,userid, password,filters):
    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()
    time.sleep(3)
    print(filters)
    all_details = []
    all_details.append([url, True,'Site Name'])
    if True:
        if 4 not in filters:
            home_page_logo = driver.find_element_by_class_name('SB-mainHeader-logo')
            home_page_logo.click()
            time.sleep(10)
            if 2 in filters:
                highlights_data = check_all_sports_data(driver, False)
                highlights_data.append('Highlights')
                print(highlights_data)
                all_details.append(highlights_data)
            if 3 in filters:
                live_now = check_all_sports_data(driver, True)
                live_now.append('Livenow')
                all_details.append(live_now)
        else:
            if 4 in filters:
                print('login=======')
                try:
                    login_detials = login1(driver, url, userid, password)
                    login_detials.append('Login')
                except Exception as error:
                    login_detials = ['Login Failed',False,'Login']
                all_details.append(login_detials)
                if login_detials[1]:
                    home_page_logo = driver.find_element_by_class_name('SB-mainHeader-logo')
                    home_page_logo.click()
                    time.sleep(10)
                    try:
                        change_language(driver)
                    except:
                        pass
                    if 2 in filters:
                        highlights_data = check_all_sports_data(driver, False)
                        highlights_data.append('Highlights')
                        all_details.append(highlights_data)
                    if 3 in filters:
                        live_now = check_all_sports_data(driver, True)
                        live_now.append('Livenow')
                        all_details.append(live_now)
                    if 5 in filters:
                        try:
                            if '//m.' in url:
                                bet_placement_data= opera_site_betplacement(driver,stake,False)
                            else:
                                bet_placement_data = bet_placement1(driver, site_name, stake, False)
                            bet_placement_data.append('Single Betplacement')
                            all_details.append(bet_placement_data)
                            if bet_placement_data[0]:
                                pass
                            else:
                                send_mail(f'Betplacement Failed in {site_name}', bet_placement_data[1])
                        except:
                            pass
                    if 12 in filters:
                        try:
                            if 'm.' in url:
                                bet_placement_data = opera_site_betplacement(driver, stake, True)
                            else:
                                bet_placement_data = bet_placement1(driver, site_name, stake, True)
                            bet_placement_data.append('Multi betPlacement')
                            all_details.append(bet_placement_data)
                            if bet_placement_data[0]:
                                pass
                            else:
                                send_mail(f'Betplacement Failed in {site_name}', bet_placement_data[1])
                        except:
                            pass
                        time.sleep(5)
                    if 9 in filters:
                        try:
                            withdraw_data = withdraw(driver)
                            withdraw_data.append('WithDraw')
                            all_details.append(withdraw_data)
                        except:
                            all_details.append(['Withdraw Failed',False,'Withdraw'])
                    if 7 in filters:
                        time.sleep(3)
                        try:
                            deposite_data = deposite(driver)
                            deposite_data.append('Deposte')
                            all_details.append(deposite_data)
                        except Exception as error:
                            print(error)
                            all_details.append(['Deposite Failed',False,'Deposte'])

                    if 8 in filters:
                        try:
                            if 'm.' in url:
                                cashout_data = opera_cashouts(driver)
                            else:
                                cashout_data =cashout(driver)
                        except Exception as error:
                            print(error)
                            cashout_data = ['Cashout Failed or no cashouts available ',False]
                        cashout_data.append('Cashout')
                        all_details.append(cashout_data)
                    if 6 in filters:
                        try:
                            jackpot_data = jackpot(driver)
                            jackpot_data.append('Jackpot')
                            all_details.append(jackpot_data)
                        except:
                            all_details.append(['Jackpot failed',False,'jackpot'])
                    if 13 in filters:
                        logout_data = logout(driver)
                        logout_data.append('Logout')
                        all_details.append(logout_data)
                        if logout_data[0]:
                            pass
                        else:
                            send_mail(f'Logout Failed in {site_name}', logout_data[1])
                else:
                    send_mail(f'Login Failed in {site_name}', login_detials[1])
    # except Exception as error:
    #     all_details.append([f'Error occured at {site_name} {str(error)}',False,'Site Error'])
    driver.close()
    print(all_details)
    return all_details


def site_number(site_number,filters):
    #a = check_site(ids)
    a = check_site(list1[site_number][0],
                   list1[site_number][1], list1[site_number][2],
                   list1[site_number][3], list1[site_number][4], filters)
    return a
#
#
# while True:
#     site_number = 2
#     a = check_site(list1[site_number][0],
#                    list1[site_number][1], list1[site_number][2],
#                    list1[site_number][3], list1[site_number][4],[4,6])
#     print(a)
#     time.sleep(60)
#     break
#
