from selenium import webdriver
import time
from check_all_sites.main import send_mail
# driver = webdriver.Chrome()
# url = 'https://www.10cric.com/'
# driver.get(url)
# driver.maximize_window()
def login(driver):
    try:
        login_ele = driver.find_elements_by_tag_name('div')
        for div_tag in login_ele:
            class_name = div_tag.get_attribute('class')
            if class_name == 'Buttonsstyles__ButtonsWrapper-sc-f5fhy1-0 kuGOCL':
                div_tag.find_element_by_tag_name('button').click()
                time.sleep(5)
                break
        login_input = driver.find_element_by_id('login')
        login_input.send_keys('TestUserSong04')
        pass_input = driver.find_element_by_id('password')
        pass_input.send_keys('123456')
        time.sleep(3)
        class_name = driver.find_element_by_class_name('notranslate')
        buttons_tag = class_name.find_elements_by_tag_name('button')
        for button in buttons_tag:
            if 'Log in' in button.text:
                button.click()
                break
        time.sleep(30)
        is_login = True
        message = 'Logged in successfully'
    except Exception as error:
        is_login= False
        message = str(error)
    return [message,is_login]


#login(driver)



def logout(driver):
    try:
        a1 = driver.find_elements_by_tag_name('nav')
        count = 0
        for a2 in a1:

            if 'Dropdownstyles__DropdownWrapper-sc-1qqkpa8-2 hHIvuX' in a2.get_attribute('class'):
                count += 1
            if count==2:
                a4 = a2.find_element_by_tag_name('div')
                a4.click()
                time.sleep(3)
                a5 = driver.find_element_by_class_name('MuiCollapse-wrapperInner')
                a6 = a5.find_elements_by_tag_name('div')
                for tag_name in a6:
                    if 'account-menu-logout' in tag_name.get_attribute('data-uat'):
                        tag_name.click()
                        time.sleep(5)
                        break
        is_logout = True
        message = 'Looged out successfully'
    except Exception as error:
        is_logout =  False
        message = str(error)
    return [message , is_logout]
#logout(driver)

#btn SB-btnOdds  SB-btnDisabled
#
def bet_placement(driver):
    print('bet placement func')
    driver.switch_to.frame('sports-client')
    time.sleep(5)
    match_boxes = driver.find_elements_by_class_name('SB-matchBox')
    click_odds = 0
    for match in match_boxes:
        odds_group = match.find_elements_by_class_name('SB-matchBox_outcomeGroup')
        for each_odds_group in odds_group:
            ui_tag = each_odds_group.find_element_by_tag_name('ul')
            li_tags = ui_tag.find_elements_by_tag_name('li')
            for li_tag in li_tags:
                odds_list = li_tag.find_elements_by_tag_name('button')
                for button in odds_list:
                    disabled_odds = 'btn SB-btnOdds'
                    if disabled_odds in button.get_attribute('class'):
                        button.click()
                        click_odds += 1
                        time.sleep(5)
                        break
                    else:
                        pass
                if click_odds >0:
                    break
            if click_odds>0:
                break
        if click_odds > 3:
            break
    time.sleep(5)
    # betslip
    bet_slip_tag = driver.find_element_by_class_name('SB-betslipBox-stakePayout-container')
    b = bet_slip_tag.find_element_by_tag_name('input')
    bc = driver.find_element_by_id('getParlayStakeId')
    value = 0
    for i in range(50):
        try:
            print(i)
            bc.clear()
            print('-----------')
            break
        except:
            value+=200
            driver.execute_script(f'window.scrollTo(0,{value});')
    time.sleep(10)
    bc.send_keys(7)
    bet_slip_button_id = driver.find_element_by_id('parlayPlacebetButtonActiveId')
    for i in range(30):
        try:
            bet_slip_button_id.click()
            print('-----------')
            break
        except:
            value += 200
            driver.execute_script(f'window.scrollTo(0,{value});')
    time.sleep(20)
    bet_placement_status = driver.find_element_by_class_name('SB-betSlip-betStatusLoader-txtContainer')
    message_text = bet_placement_status.text
    print(message_text)


#bet_placement(driver)
#time.sleep(10)
# driver.close()

def check_site(site_name,url,userid,password,stake):
    driver = webdriver.Chrome(r'C:\Users\User 101\Desktop\automation projects\cricket_scrape_site\chromedriver.exe')
    driver.get(url)
    driver.maximize_window()
    time.sleep(3)
    login_status = login(driver)
    if login_status[1]:
        time.sleep(5)
        logout_status = logout(driver)
        if login_status[1]:
            pass
        else:
            send_mail(f'Logout Failed in {site_name}',logout_status[0])
    else:
        send_mail(f'Login Failed in {site_name}',login_status[0])
    driver.close()