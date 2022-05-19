from selenium import webdriver
import time

url = 'http://137.116.173.46:15672/#/queues'

def login(driver):
    userid = 'support'
    password = '#@!$upport*()'
    input_tags = driver.find_elements_by_tag_name('input')
    input_tags[0].send_keys(userid)
    input_tags[1].send_keys(password)
    time.sleep(3)
    input_tags[2].click()
    time.sleep(5)


def purge_page(driver):
    legend_tag = driver.find_elements_by_class_name('legend')[1]
    list_values = []
    list_values.append(legend_tag.text)
    print(list_values)
    a5 = str(list_values).index('Total')
    a6 = int(str(list_values)[a5 + 7:-2].replace(',', ''))
    p1 = driver.find_elements_by_tag_name('div')
    driver.execute_script(f'window.scrollTo(0,3000)')
    time.sleep(3)
    a = driver.find_elements_by_tag_name('h2')
    if True:
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
            #driver.switch_to_alert().accept()
            driver.switch_to_alert().dismiss()
            time.sleep(2)
            purge_main_tag.click()
            time.sleep(3)


def purge_home_page(driver,count_tag):
    count_of_ques = 0
    all_list_tags = driver.find_element_by_class_name('list')
    table_body_tag = all_list_tags.find_element_by_tag_name('tbody')
    tr_tag = table_body_tag.find_elements_by_tag_name('tr')
    down_cursor = count_tag
    if True:
        down_cursor+=1
        value1 = down_cursor*600
        count = 0
        td_tag = tr_tag[count_tag].find_elements_by_tag_name('td')
        for j in td_tag:
            count+=1
            if count==6:
                values = int(str(j.text).replace(',',''))
                if values>=count_of_ques:
                    td_tag[0].click()
                    time.sleep(3)
                    purge_page(driver)
                    time.sleep(3)
                    tabs_tag = driver.find_element_by_id('tabs')
                    tabs_li_tag = tabs_tag.find_elements_by_tag_name('li')
                    for list_value in tabs_li_tag:
                        if 'Queues' in list_value.text:
                            list_value.click()
                            break
                    driver.execute_script(f'window.scrollTo(0,-{down_cursor})')
                    time.sleep(3)


def run_purge_test():
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)
    try:
        login(driver)
        for number_of_times in range(10):
            print(number_of_times)
            time.sleep(3)
            list_tag = driver.find_element_by_class_name('list')
            tbody_tag = list_tag.find_element_by_tag_name('tbody')
            tr_tags = tbody_tag.find_elements_by_tag_name('tr')
            for count_of_tags in range(len(tr_tags)):
                purge_home_page(driver, count_of_tags)
    except:
        pass
    driver.quit()

#run_purge_test()
