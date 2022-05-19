from selenium import webdriver
from check_all_sites.main import send_mail
import time
from check_all_sites.tenbet_datachecks import  check_all_sports_data


url1 = 'https://10bet.co.tz/login?overrideregion=true'
url2 = 'https://10bet.com.gh/login?overrideregion=true'
url3 = 'https://10bet.co.zm/login?overrideregion=true'
url4 = 'https://10betdrc.com/login?overrideregion=true'

url1_opera = 'https://m.10bet.co.tz/login?overrideregion=true'
url2_opera = 'https://m.10bet.com.gh/login?overrideregion=true'
url3_opera = 'https://m.10bet.co.zm/login?overrideregion=true'
url4_opera = 'https://m.10betdrc.com/login?overrideregion=true'

userid_1 = 765765765
password_1 = 1234

userid_2 = 245245245
password_2 = 1234

userid_3 = 962962962
password_3 = 1234

userid_4 = 840840840
password_4 = 1234



def login(driver, url, user_id, password):
    try:
        time.sleep(3)
        userid_input = driver.find_element_by_id('userMobileNo')
        password_input = driver.find_element_by_id('userPassword')
        userid_input.send_keys(user_id)
        password_input.send_keys(password)
        time.sleep(2)
        login_box = driver.find_element_by_id('disableLoginButtonClick')
        login_box.click()
        time.sleep(5)
        error_message = driver.find_element_by_id('loginErrorMessage')
        message = error_message.text
        print('--==============', message)
        if len(message) > 0:
            message = message
        else:
            message = 'Login Success'
        driver.refresh()
        time.sleep(8)
        is_login = False
        print('--------------------------------')
        try:
            time.sleep(5)
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
    return [message,is_login]

def logout(driver):
    try:
        balance_button = driver.find_element_by_class_name('SB-dropdown-btn')
        balance_button.click()
        time.sleep(15)
        a = driver.find_element_by_class_name("SB-myAccountList")
        a1 = a.find_elements_by_class_name('SB-myAccountList-item')
        a2 = a1[-1].find_element_by_class_name('SB-myAccountList-item-content')
        a3 = a2.find_element_by_tag_name('a')
        a3.click()
        time.sleep(10)
        is_logout = True
        logout_message = 'Logout Done'
    except Exception as error:
        logout_message = str(error)
        is_logout = False
    return [logout_message,is_logout]


def bet_placement1(driver,site_name,stake,is_multibet):
    try:
        live_match_button = driver.find_element_by_id('livenow')
        a_tag = live_match_button.find_element_by_tag_name('a')
        a_tag.click()
        time.sleep(3)
        y_axis = 100
        count = 0
        button_click= False
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
                        count +=1
                        break
                    break
                except:
                    y_axis += 200
            if is_multibet:
                if count>2:
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
        is_bet = False
        message = 'Bet placement is failed'
    return [message,is_bet]



def check_site(url, userid, password, stake, site_name):
    driver = webdriver.Chrome(r'C:\Users\User 101\Desktop\automation projects\cricket_scrape_site\chromedriver.exe')
    driver.get(url)
    driver.maximize_window()
    time.sleep(3)
    login_status = login(driver,url,userid,password)
    try:
        if login_status[1]:
            home_page_logo = driver.find_element_by_class_name('SB-mainHeader-logo')
            home_page_logo.click()
            time.sleep(10)
            hours = time.strftime('%H')
            minutes = time.strftime('%M')

            bet_status = ['Betfailed', False]

            if int(hours) % 6 == 0:

                if int(minutes) > 3 and int(minutes) <= 10:
                    for i in range(3):
                        bet_status = bet_placement1(driver,site_name, stake, False)
                        if bet_status[1]:
                            break
                        else:
                            pass
                    if bet_status[1]:
                        pass
                    else:
                        send_mail(f'Betfailed in {site_name}', bet_status[0])

                    bet_status = ['Betfailed', False]
                    if int(hours) % 6 == 0:
                        for i in range(3):
                            bet_status = bet_placement1(driver, site_name, stake, True)
                            if bet_status[1]:
                                break
                            else:
                                pass
                        if bet_status[1]:
                            pass
                        else:
                            send_mail(f'Betfailed in {site_name}', bet_status[0])

            logout_status = logout(driver)
            if logout_status[1]:
                pass
            else:
                send_mail(f'Logout failed at {site_name}',logout_status[0])
    except Exception as error:
        send_mail(f'{site_name} Site not loading ',str(error))

    driver.close()