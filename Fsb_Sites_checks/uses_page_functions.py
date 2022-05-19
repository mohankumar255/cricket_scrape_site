from selenium import webdriver
import time


def bet_placement123(driver,url,stake_amount,is_multibet):
    a=driver.find_element_by_id('liveMatches')
    a.click()
    time.sleep(5)
    login_status = False
    bet_placement_status=False
    balance = ''
    message=''
    active_odds_count=0
    try:
        if True:
            bet_place_status = True
    except Exception as error:
        bet_place_status = True
        # log_file('fsb_logs', '--------------Erorr---------')
        # log_file('fsb_logs', f'--------------{url}---------')
        # log_file('fsb_logs', str(error))
        # log_file('fsb_logs', '------------------this  error occurred at deposite button------------------')
        # notification(f'please check {url} login')
        # --------------
    try:
        if bet_place_status:
            # ------this is for notification button to refuse the notifications
            # -------------------------------------------
            a=driver.find_element_by_class_name("BLM-content")

            b=a.find_elements_by_tag_name('div')
            for i in b:
                c=i.get_attribute('class')
                if c=='BLM-leagueBox BLM-accordion':
                    d=i.find_element_by_class_name('BLM-leagueBox-header__leagueInfo')
                    print(d.text)

                    if ' E-Soccer' in d.text:
                        pass
                    else:
                        match = i.find_elements_by_class_name('BLM-matchBox')
                        print(len(match))
                        count = 0
                        click_odds_count = 0
                        for j in match:
                            odds_values = j.find_elements_by_class_name('BLM-btnOddsGroup')
                            for i in odds_values:
                                li_value = i.find_element_by_tag_name('li')
                                odds_button_tag = j.find_element_by_tag_name('button')
                                odds_button_status = odds_button_tag.get_attribute('class')

                                if 'btn BLM-btnOdds BLM-btnOddsDisabled' in odds_button_status:
                                    pass
                                else:
                                    message=(i.text)
                                    if True:
                                        time.sleep(2)
                                        #driver.execute_script('window.scrollTo(0,300);')
                                        #time.sleep(2)
                                        active_odds_count=1
                                        value=0
                                        while True:
                                            value+=100
                                            try:
                                                odds_button_tag.click()
                                                click_odds_count += 1
                                                break
                                            except:
                                                driver.execute_script(f'window.scrollTo(0,{value})')
                                        break
                            if is_multibet:
                                if len(match) >= 4:
                                    if click_odds_count == 4:
                                        break
                                else:
                                    pass
                            else:
                                break
                        #driver.execute_script('window.scrollTo(0,-10);')
                        if click_odds_count>=1:
                            time.sleep(5)
                            bet_slip_tag = driver.find_element_by_id('BLM-betSlip-Button')
                            bet_slip_tag.click()
                            time.sleep(5)
                            stake_tag = driver.find_element_by_id('stakeValue')
                            stake_tag.clear()
                            stake_tag.send_keys(stake_amount)
                            bet_place_button_tag = driver.find_element_by_id('disablePlaceBetButton')
                            bet_place_button_tag.click()
                            time.sleep(30)
                            try:
                                try:
                                    bet_status_tag = driver.find_element_by_class_name('BLM-betReceipt-betSuccess')
                                    bet_status = bet_status_tag.text
                                    if is_multibet:
                                        message='Your MultiBet:'+bet_status
                                    else:
                                        message=bet_status
                                    print(message)
                                    # log_file('fsb_logs', f'--------------{url}---------')
                                    # log_file('fsb_logs', f'--------------{bet_status}---------')
                                    close_receipt = driver.find_element_by_class_name('BLM-betReceipt-btnClose')
                                    close_receipt.click()
                                    print('betlion')
                                    time.sleep(5)
                                    bet_placement_status=True
                                except:
                                    bet_status_tag = driver.find_element_by_class_name('BLM-betReceipt-betSuccessMsg')
                                    bet_status = bet_status_tag.text
                                    message = (bet_status)
                                    print(message)
                                    # log_file('fsb_logs', f'--------------{url}---------')
                                    # log_file('fsb_logs', f'--------------{bet_status}---------')
                                    close_receipt = driver.find_element_by_class_name('BLM-betReceipt-btnClose')
                                    close_receipt_button = close_receipt.find_element_by_tag_name('button')
                                    close_receipt_button.click()
                                    bet_placement_status=True
                                    time.sleep(5)
                            except Exception as error:
                                print(error)
                                error_message=driver.find_element_by_id('placeBetErrorMessageDisplay')
                                span_tag=error_message.find_element_by_tag_name('span')
                                span_tag_message=error_message.text
                                message=span_tag_message
                                print(span_tag_message)
                                close_receipt_button=driver.find_element_by_class_name('BLM-betSlip-closeButton')
                                #close_receipt_button=close_receipt.find_element_by_tag_name('button')
                                close_receipt_button.click()
                                bet_placement_status=False
                                # notification('bet rejected')
                                # log_file('fsb_logs', '----------error-----------------')
                                # log_file('fsb_logs', f'bet rejected for {url}')
                                # log_file('fsb_logs', f'----------{message}-----------------')
                                #driver.find_element_by_id('BLM-betSlip-closeButton').click()
                                time.sleep(5)
                                print(message)
                        break
        if active_odds_count >= 1:
            pass
        else:
            bet_placement_status=False
            message=('There are No active odds for first active sports')
    except Exception as error:
        print(error)
        message = 'Error occured at Betplacement'
        # log_file('fsb_logs',message)
        # log_file('fsb_logs',str(error))
        bet_placement_status=False
    print(message,bet_placement_status)
    return [message,bet_placement_status]

def login(driver,  user_id,  password):
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
            return [message,   True]
        else:
            error_message = driver.find_element_by_id('displayErrorMessage')
            message = error_message.find_element_by_tag_name('span')
            message = message.text
            return [message,   False]
    #  except:
    #
    #      return [message,   False]
driver=webdriver.Chrome()
driver.get('')