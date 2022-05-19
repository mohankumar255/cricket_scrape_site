from selenium import webdriver
import time
from Fsb_Sites_checks.comman_use_libraries import *
from Fsb_Sites_checks.data_checks_functions import *
from Fsb_Sites_checks.Feed_checks import live_matches_all_event_ids


def register(url, driver, user_id, password):
    value = 0
    try:
        register = driver.find_element_by_class_name('BLM-mainHeader-loginRegister')
        a_tag = register.find_elements_by_tag_name('a')
        a_tag = a_tag[1]
        register_button = a_tag.find_element_by_tag_name('button')
        register_button.click()
        time.sleep(5)
        # reg_page_title = driver.find_element_by_class_name('BLM-pageTitle')
        # message = (reg_page_title.text)
        mobile_id_tag = driver.find_element_by_id('regMobile')
        mobile_id_tag.send_keys(user_id)
        pass1_tag = driver.find_element_by_id('regPass')
        pass1_tag.send_keys(password)
        pass2_tag = driver.find_element_by_id('regConfirm')
        pass2_tag.send_keys(password)
        value = 200
        while True:
            value += 200
            try:
                driver.execute_script(f'window.scrollTo(0,  {value});')
                sign_up_button_tag = driver.find_element_by_id('disableRegisterButtonClick')
                sign_up_button_tag.click()
                break
            except Exception as error:
                pass
        time.sleep(5)
        try:
            error_msg = driver.find_element_by_class_name('showApiErrorMessage')
            message = (error_msg.text)
            register_status = False
        except Exception as error:
            error_message = driver.find_element_by_id('showApiErrorMessage')
            message = error_message.text
            register_status = False
            pass
        time.sleep(5)
    except Exception as error:
        print(error)
        message = 'error occurred at regester button'
        time.sleep(5)
        register_status = False
    driver.execute_script(f'window.scrollTo(0,  -{value});')
    time.sleep(3)
    print(message, register_status)
    return [message, register_status]


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


def deposit(driver):
    x = driver.find_element_by_class_name('BLM-mainHeader-freeBetDeposit')
    deposit_button = x.find_element_by_tag_name('button')
    deposit_button.click()
    time.sleep(5)
    deposit_amount_button = driver.find_element_by_id('disableDepositButtonClick')
    deposit_amount_button.click()
    time.sleep(5)
    try:
        try:
            message = driver.find_element_by_class_name('BLM-pageTitle')
            success_message = message.text
            message = success_message
        except:
            message = driver.find_element_by_class_name('BLM-pageHeader-title')
            success_message = message.text
            message = success_message
        deposite = True
    except:
        message = 'Error occured at deposite'
        deposite = False
        pass
    click_home_page(driver)
    return [message, deposite]


def my_bet_slip(driver):
    bet_slip_tag = driver.find_element_by_class_name('BLM-categoryGridItem')
    a_tag = bet_slip_tag.find_element_by_tag_name('a')
    a_tag.click()
    time.sleep(5)
    cash_out_button = driver.find_element_by_id('cashoutAddActive')
    cash_out_text = cash_out_button.text
    message = cash_out_text
    value = 0
    cash_out_status = False
    try:
        if 'Cash Out' in cash_out_text:
            cash_out_button.click()
            time.sleep(5)
            cashout_bet_count = 0
            while True:
                value += 200
                print(value)
                try:
                    driver.execute_script(f'window.scrollTo(0,  {value});')
                    cash_out_buttons = driver.find_elements_by_class_name('BLM-cashOut-container')
                    if len(cash_out_buttons) >= 1:
                        for cash_out_button in cash_out_buttons:
                            if 'Cashout' in cash_out_button.text:
                                cash_out_button.click()
                                time.sleep(5)
                                confirm_button = cash_out_button.find_elements_by_tag_name('button')
                                confirm_button[1].click()
                                message = 'cash out done'
                                back_btn = driver.find_element_by_class_name('BLM-pageBackButton')
                                back_btn.click()
                                time.sleep(3)
                                cash_out_status = True
                                cashout_bet_count += 1
                                break
                            if cashout_bet_count >= 1:
                                break
                        else:
                            next_button = driver.find_element_by_class_name('class')
                            next_button.click()
                    else:
                        message = 'There are no cashouts available'
                        back_btn = driver.find_element_by_class_name('BLM-pageBackButton')
                        back_btn.click()
                        time.sleep(5)
                        cash_out_status = True
                    break
                except Exception as error:
                    print(error)
                    print(value)
                    if value == 20000:
                        break
                    pass
        else:
            cash_out_status = False
            message = ('cash out fail')
            back_btn = driver.find_element_by_class_name('BLM-pageBackButton')
            back_btn.click()
            time.sleep(5)
    except:
        cash_out_status = False
        message = 'Error occured at Cashout'
        my_account_tab(driver)
    return [message, cash_out_status]


def jackpot_page(driver, url, stake_amount):
    print('hello mohan')
    # header_button = driver.find_element_by_class_name('BLM-hamBurger-menu')
    # header_button.click()
    # time.sleep(5): 
    jackpot_option = False
    c = driver.find_elements_by_tag_name('a')
    for i in c:
        d = i.get_attribute('href')
        if d:
            if '/Jackpot' in d:
                i.click()
                time.sleep(5)
                jackpot_option = True
                break
    if jackpot_option:
        try:
            try:
                play_jackpot = driver.find_element_by_class_name('NP-cardBanner__actions')
                play_jackpot_button = play_jackpot.find_element_by_tag_name('button')
                play_jackpot_button.click()
            except:
                play_jackpot = driver.find_element_by_class_name('BLM-card-body')
                play_jackpot_button = play_jackpot.find_element_by_tag_name('button')
                play_jackpot_button.click()
            time.sleep(5)
            a = driver.find_element_by_class_name('BLM-filterButtons')
            b = a.find_elements_by_tag_name('li')
            b[0].click()
            time.sleep(5)
            count = 500
            while True:
                try:
                    count += 100
                    driver.execute_script(f'window.scrollTo(0,  {count});')
                    c = driver.find_element_by_id('saveButton')
                    c.click()
                    time.sleep(3)
                    break
                except:
                    count += 100
                    driver.execute_script(f'window.scrollTo(0,  {count});')
            try:
                close_receipt = driver.find_element_by_class_name('BLM-betReceipt-btnClose')
                close_receipt.click()
                message = ('Jackpot bet placed successfully')
                jackpot_status = True
            except Exception as error:
                print(error)
                error_message = driver.fin
                message = ('Jackpot Failed')
                jackpot_status = False


        except Exception as error:

            message = ('There is no jackpot available')
            jackpot_status = True
        print(message, jackpot_status)
        return [message, jackpot_status]
    else:
        return ['We are not support Jackport for this site', True]


def highlights(driver, site_name):
    driver.find_element_by_id('highlights').click()
    time.sleep(5)
    messages = []
    try:
        a = driver.find_element_by_class_name('upcomingTimeList')
        b = a.find_elements_by_tag_name('li')
        no_matches_count = 0
        for i in b:
            i.click()
            time.sleep(3)
            odds_active = odds_active_or_not(driver,site_name)
            # check_data_time = check_date_time_past_data_or_not(driver,  site_name)
            if len(odds_active) > 0:
                messages.append(odds_active)
                no_matches_count += 1
            # if len(check_data_time) > 0:
            #     messages.append(check_data_time)
            #     no_matches_count += 1
            try:
                c = driver.find_elements_by_class_name('BLM-matchBox')
                if len(c) >= 1:
                    message1 = f'Matches are available in highlights under {i.text}'
                else:
                    no_matches_count += 1
                    message1 = f'Matches are not available in highlights under {i.text}'
                messages.append(message1)
            except Exception as error:
                print(error)
                message = i.text
                print(message)
                message = 'Error occurred at Highlightes'
                # notification('Error occurred at Highlightes')

                highlights_status = False
                messages = [message]
        if no_matches_count >= 1:
            highlights_status = False
        else:
            highlights_status = True
        messages = [messages, highlights_status]
    except:
        message = []
        if True:
            message1 = odds_active_or_not(driver,site_name)
            # message2 = check_date_time_past_data_or_not(driver,  site_name)
            if len(message1) == 0:
                pass
            else:
                message.append(message1)
            # if len(message2) == 0:
            #     pass
            # else:
            #     message.append(message2)
            c = driver.find_elements_by_class_name('BLM-matchBox')
            no_matches_count = 0
            if len(c) >= 1:
                message1 = 'There are matches for Highlights for Top Games'
            else:
                no_matches_count += 1
                message1 = 'There are no matches for highlights for Top Games'
            a = driver.find_element_by_class_name('PopularTabslist')
            b = a.find_elements_by_tag_name('li')
            c = b[-1].click()
            time.sleep(3)
            c = driver.find_elements_by_class_name('BLM-matchBox')
            if len(c) >= 1:
                odds_active_list = odds_active_or_not(driver,site_name)
                # check_date_time = check_date_time_past_data_or_not(driver,   site_name)
                if len(odds_active_list) > 0:
                    message.append(odds_active_list)
                    no_matches_count += 1
                # if len(check_date_time) >0:
                #     message.append(check_date_time)
                #     no_matches_count += 1
                message2 = 'There are matches for Highlights for Trending'
            else:
                no_matches_count += 1
                message2 = 'There are no matches for highlights for Trending'
            message = message + [message1, message2]
            if no_matches_count >= 1:
                highlights_status = False
            else:
                highlights_status = True
            messages = [message, highlights_status]
        #   except Exception as error:
        #      print(error)
        #      message = 'Error occurred at Highlights tab'
        #      # notification('Error occurred at Highlights')
        #      log_file('fsb_logs',  'Error occurred at Highlights')
        #      log_file('fsb_logs',  str(error))
        #      messages = [message,  False]
    return messages


def livenow(driver, site_name):
    a = driver.find_element_by_id('liveMatches')
    a.click()
    time.sleep(5)
    messages = []

    try:
        message = odds_active_or_not(driver,site_name)
        if len(message) == 0:
            pass
        else:
            messages.append(message)
        c = driver.find_elements_by_class_name('BLM-matchBox')
        message = (len(c))
        live_now_matches = True
        if len(c) >= 1:
            message = 'there are matches for Livenow'
        else:
            live_now_matches = False
            message = 'there are no matches for Live now'
    except Exception as error:
        print(error)
        live_now_matches = False
        message = 'Error occurred at Live now Tab'
    message1 = live_now_data_check(driver, site_name)
    messages.append(message)
    if len(message1[0]) > 0 or len(message1[1]) > 0:
        messages.append(message1)
        live_now_matches = False
    return [messages, live_now_matches]


def cashout_11(driver):
    bet_slip_tag = driver.find_element_by_class_name('BLM-categoryGridItem')
    a_tag = bet_slip_tag.find_element_by_tag_name('a')
    a_tag.click()
    time.sleep(5)
    cash_out_button = driver.find_element_by_id('cashoutAddActive')
    cash_out_text = cash_out_button.text
    message = (cash_out_text)
    cash_out_status = False
    if 'Cash Out' in cash_out_text:
        cash_out_button.click()
        time.sleep(5)
        len_of_cashouts = []
        cash_out_button = driver.find_elements_by_class_name('BLM-cashOut-container')
        a1 = []
        for i in cash_out_button:
            print(i.text)
        length = (len(cash_out_button))
        cash_out_done = 0
        no_of_checks = 0
        value = 0
        if length >= 2:
            while True:
                value += 200
                print(value)
                try:
                    driver.execute_script(f'window.scrollTo(0,  {value});')
                    for i in range(2):
                        while True:
                            for i in cash_out_button:
                                try:
                                    button = i.find_element_by_tag_name('button')
                                    button.click()
                                    time.sleep(3)
                                    break
                                except:
                                    no_of_checks += 1
                                    if no_of_checks == 10:
                                        break
                                    pass
                            break
                    no_of_checks = 0
                    while True:
                        for i in cash_out_button:
                            try:
                                button = i.find_elements_by_tag_name('button')
                                button[1].click()
                                time.sleep(3)
                                message = 'Cashout Done'
                                cash_out_status = True
                                cash_out_done += 1
                                length_of_cashouts = driver.find_elements_by_class_name(
                                    'BLM-cashOut-container')
                                if len(length_of_cashouts) == length:
                                    message = 'Cashout done ,  but cashout not valid'
                                else:
                                    message = 'Cashout done'

                                break
                            except:
                                no_of_checks += 1
                                if no_of_checks == 10:
                                    break
                                pass
                        break
                    break
                except:
                    pass
        else:
            message = ('There are no cashouts available')

            cash_out_status = True
    return [message, cash_out_status]


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


def chat_box(driver):
    chat_box_tag = driver.find_element_by_id('open_fc_widget')
    chat_box_tag.click()
    time.sleep(60)
    if True:
        try:
            write_comment_tag = driver.find_elements_by_tag_name('textarea')
            write_comment_tag = write_comment_tag[1]
            write_comment_tag.send_keys('Hello Team')
            time.sleep(2)
            send_div_tag = driver.find_element_by_class_name('tawk-chatinput-send-container')
            send_button_tag = send_div_tag.find_element_by_tag_name('button')
            send_button_tag.click()
            print(
                ' == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ')
        except:
            pass
    print(' == == == == == == == == == == == == == == == ')
    time.sleep(10)


def upcoming(driver, site_name):
    time.sleep(3)
    upcoming_click_id = 'upcomingMatches'
    driver.find_element_by_id(upcoming_click_id).click()
    time.sleep(5)
    disbale_header_notification(driver)
    id_name = 'ddn_upcomingsportlist'
    filter_id_tag = driver.find_element_by_id(id_name)
    option_tags = len(filter_id_tag.find_elements_by_tag_name('option'))
    values = []
    list_sport_unavailable_matches = []
    messages = []
    for i in range(option_tags):
        try:
            id_name = 'ddn_upcomingsportlist'
            filter_id_tag = driver.find_element_by_id(id_name)
            option_tags = filter_id_tag.find_elements_by_tag_name('option')
            select_sport_tag = option_tags[i]
            select_sport_tag.click()
            sport_name = select_sport_tag.text
            values.append(sport_name)
            time.sleep(3)
            time_select_class_tag = 'upcomingTimeList'
            length_of_list_tag = driver.find_element_by_class_name(time_select_class_tag)
            list_element_tags = length_of_list_tag.find_elements_by_tag_name('li')
            missing_matches_count = 0
            for list_tag in range(len(list_element_tags)):
                time_select_class_tag = 'upcomingTimeList'
                length_of_list_tag = driver.find_element_by_class_name(time_select_class_tag)
                list_element_tags = length_of_list_tag.find_elements_by_tag_name('li')
                time_tag = list_element_tags[list_tag]
                time_tag.click()
                time_tag_name = time_tag.text
                time.sleep(3)
                duplicate_odds_list = odds_active_or_not(driver,site_name)
                if len(duplicate_odds_list) > 0:
                    messages.append(duplicate_odds_list)
                a1 = 'BLM-matchBox'
                length = driver.find_elements_by_class_name(a1)
                if len(length) > 0:
                    pass
                else:
                    missing_matches_count += 1
            if missing_matches_count > 2:
                list_sport_unavailable_matches.append(
                    [sport_name, time_tag_name, 'matches not availble'])
        except:
            pass
    if len(list_sport_unavailable_matches) > 0:
        is_matches_missing = False
    else:
        list_sport_unavailable_matches.append('Matches are availble in upcoming tab')
        is_matches_missing = True
    if len(messages) > 0:
        is_matches_missing = False
        list_sport_unavailable_matches.append(messages)
    return [list_sport_unavailable_matches, is_matches_missing]


def betyetu_upcoming(driver, site_name):
    time.sleep(3)
    upcoming_click_id = 'upcomingMatches'
    driver.find_element_by_id(upcoming_click_id).click()
    time.sleep(3)
    drop_down_id_tag = 'ddn_leagues'
    drop_down_tag = driver.find_element_by_id(drop_down_id_tag)
    option_tags = drop_down_tag.find_elements_by_tag_name('option')
    is_matches_available = True
    list_sport_unavailable_matches = []
    for i in range(len(option_tags)):
        drop_down_id_tag = 'ddn_leagues'
        drop_down_tag = driver.find_element_by_id(drop_down_id_tag)
        option_tags = drop_down_tag.find_elements_by_tag_name('option')
        league_name_tag = option_tags[i]
        league_name_tag.click()
        time.sleep(3)
        time_id_tags = 'ddn_upcomingdayfilters'
        filters_tag_list = driver.find_element_by_id(time_id_tags)
        list_values = filters_tag_list.find_elements_by_tag_name('option')
        missing_matches_count = 0
        for j in range(len(list_values)):
            time_id_tags = 'ddn_upcomingdayfilters'
            filters_tag_list = driver.find_element_by_id(time_id_tags)
            list_values = filters_tag_list.find_elements_by_tag_name('option')
            time_tag = list_values[j]
            time_tag.click()
            time.sleep(5)
            duplicate_odds_list = odds_active_or_not(driver, site_name)
            print(duplicate_odds_list)
            message_content_element = driver.find_element_by_class_name("BLM-content")
            message_element = message_content_element.find_element_by_tag_name('div')
            if 'd-none' in message_element.get_attribute('class'):
                pass
            else:
                missing_matches_count += 1
        if missing_matches_count > 2:
            list_sport_unavailable_matches.append(
                [league_name_tag.text, 'matches not availble'])
    is_matches_missing = False
    if len(list_sport_unavailable_matches) > 0:
        is_matches_missing = False
    else:
        list_sport_unavailable_matches.append('Matches are availble in upcoming tab')
        is_matches_missing = True
    return [list_sport_unavailable_matches, is_matches_missing]


def site_checks(site_name, url, user_id, password, stake_amount, filters):
    all_checks_status = []
    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()
    time.sleep(3)
    try:
        login_status = ['Not Logged Into Site', False]
        start_time = time.time()
        all_checks_status.append([url, True])
        if 'betyetu' in url:
            select_language(driver)
        disbale_header_notification(driver)
        if 'parimatch' in url:
            pass
        else:
            # pass
            if 1 in filters:
                all_checks_status.append(register(url, driver, user_id, password))
        disbale_header_notification(driver)
        click_home_page(driver)
        start_time1 = time.time()
        if 11 in filters:
            if 'betlion' in url:
                all_checks_status.append(upcoming(driver, site_name))
            else:
                all_checks_status.append(betyetu_upcoming(driver, site_name))
        if 2 in filters:
            all_checks_status.append(highlights(driver, site_name))
        if 3 in filters:
            all_checks_status.append(livenow(driver, site_name))
        disbale_header_notification(driver)
        if 4 in filters:
            login_status = login(driver, user_id, password)
            print(login_status)
        if login_status[1]:
            time.sleep(10)
            all_checks_status.append(login_status)
            disable_footer_notification(driver)
            if 5 in filters:
                # all_checks_status.append(bet_placement(driver,  url,  stake_amount,  True))
                all_checks_status.append(bet_placement123(driver, url, stake_amount, False))
            if 12 in filters:
                all_checks_status.append(bet_placement123(driver, url, stake_amount, True))
            if 6 in filters:
                try:
                    all_checks_status.append(jackpot_page(driver, url, stake_amount))
                except:
                    pass
            if 7 in filters:
                all_checks_status.append(deposit(driver))
            if 8 in filters:
                my_account_tab(driver)
                if 'betlion' in url:
                    all_checks_status.append(my_bet_slip(driver))
                    time.sleep(5)
                else:
                    all_checks_status.append(cashout_11(driver))
                click_home_page(driver)
            disbale_header_notification(driver)
            disable_footer_notification(driver)
            click_home_page(driver)
            if 9 in filters:
                my_account_tab(driver)
                try:
                    all_checks_status.append(logout(driver))
                except Exception as error:
                    print(error)
                    all_checks_status.append(['Error occured at logout', False])
        else:
            print(login_status[0])
            all_checks_status.append(login_status)
    except Exception as error:
        print(error)
        # notification('login failed')
        all_checks_status.append([f'Error occured at {url}', False])
    driver.close()
    return all_checks_status

# print(site_checks('betlion',  'https://mobile.betlion.ke',  '900123123',  '0000',  2, [1]))
# site_checks('betyetu',  'https://betyetu.co.mz/',  847479080,  '2311',  10, [4,5])
# site_checks(betlion, 'https://m.betlion.co.zm',  '722559551',  '3684',  2)
# site_checks('playabet', 'https://playabet.co.ke/',  '742537331',  '1234',  10, [4, 9])
# site_checks('fjjf', 'https://parimatch.com.gh/',  '233123456',  '0000',  10,[4,5])
# site_checks('mkekabet','https://m.mkekabet.com/',  '752580000',  '1234',  10,[2])
