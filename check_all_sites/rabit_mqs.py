from selenium import webdriver
import time
from logging import *

url = 'http://137.116.173.46:15672/#/queues'
userid = 'support'
password = '#@!$upport*()'
count_of_ques = 0


def log_file(message):
    date = time.strftime('%y-%m-%d')
    file1 = open('sample.txt', 'a')
    file1.write(date + '************************* ' + message)
    file1.write('\n')
    file1.close()
    file_name = f'fsb_logs/{date}.log'
    format = '%(lineno)s *** %(name)s *** %(asctime)s *** %(message)s'
    # logger = logging.getLogger()
    basicConfig(filename=file_name, filemode='a', format=format, level=DEBUG)
    info(message)


# log_file('hello')

def login(driver):
    # to access the input tags for userid ,password and submit button
    try:
        input_tags = driver.find_elements_by_tag_name('input')
        input_tags[0].send_keys(userid)
        input_tags[1].send_keys(password)
        time.sleep(3)
        input_tags[2].click()
        time.sleep(5)
        log_file('Rabit mq site is logged in successfully')
        is_login = True
        message = 'Login successfullu'
    except Exception as err:
        is_login = False
        message = 'Login Failed ' + str(err)
        log_file(message)
    return [is_login, message]


def purge_page(driver):
    legend_tag = driver.find_elements_by_class_name('legend')[1]
    list_values = []
    list_values.append(legend_tag.text)
    print(list_values)
    driver.execute_script(f'window.scrollTo(0,3000)')
    time.sleep(3)
    a = driver.find_elements_by_tag_name('h2')
    name_of_property = driver.find_element_by_id('main')
    h1_tag = name_of_property.find_element_by_tag_name('h1').text
    for purge_main_tag in a:
        if purge_main_tag.text == 'Purge':
            purge_main_tag.click()
            time.sleep(3)
            break
    p2 = driver.find_elements_by_tag_name('input')
    for name in p2:
        if 'Purge' in name.get_attribute('value'):
            name.click()
            time.sleep(3)

            # these two used to dismiss and accept the popup message
            # when we want test real time need to enable accept method and disable dismiss method

            print(h1_tag)
            driver.switch_to_alert().dismiss()
            log_file(f'we are not accept the purging for {h1_tag}')
            # driver.switch_to_alert().accept()
            # log_file(f'we are accepting the purging for {h1_tag}')
            time.sleep(2)
            purge_main_tag.click()
            time.sleep(3)


def purge_home_page(driver, count_tag):
    # count tag used to click on the elements on name tag.
    all_list_tags = driver.find_element_by_class_name('list')
    table_body_tag = all_list_tags.find_element_by_tag_name('tbody')
    tr_tag = table_body_tag.find_elements_by_tag_name('tr')
    down_cursor = count_tag
    down_cursor += 1
    count = 0
    td_tag = tr_tag[count_tag].find_elements_by_tag_name('td')
    for j in td_tag:
        count += 1
        if count == 6:
            values = int(str(j.text).replace(',', ''))
            # if values number is more than or equal to will click on name properti
            if values >= count_of_ques:
                name = td_tag[0].find_element_by_tag_name('a').text
                td_tag[0].click()
                time.sleep(5)
                log_file(f'The count of {name} is {values}')

                # this is purge page which after clicking
                purge_page(driver)
                time.sleep(3)
                tabs_tag = driver.find_element_by_id('tabs')
                tabs_li_tag = tabs_tag.find_elements_by_tag_name('li')
                for list_value in tabs_li_tag:
                    if 'Queues' in list_value.text:
                        list_value.click()
                        break
                driver.execute_script(f'window.scrollTo(0,-{down_cursor * 500})')
                time.sleep(3)


def run_purge_test():
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)
    try:
        login_status = login(driver)
        if login_status[0]:

            # This for loop used to peroform the action continuoesly
            for number_of_times in range(1):
                time.sleep(3)
                list_tag = driver.find_element_by_class_name('list')
                tbody_tag = list_tag.find_element_by_tag_name('tbody')
                tr_tags = tbody_tag.find_elements_by_tag_name('tr')
                count = 0
                for count_of_tags in range(len(tr_tags)):
                    purge_home_page(driver, count_of_tags)
        else:
            log_file(login_status[1])

    except Exception as err:
        print(err)
        log_file(str(err))
        pass
    driver.quit()


#run_purge_test()
