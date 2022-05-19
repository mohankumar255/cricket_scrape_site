from selenium import webdriver
import time,datetime




#dri=webdriver.Chrome()
#driver.get('https://www.10cric.com/')
'''
a=driver.find_element_by_xpath('//*[@id="__next"]/header/div/div[3]/button')

a.click()
time.sleep(3)

b=driver.find_element_by_id('login')
b.send_keys('TestUserSong04')
c=driver.find_element_by_id('password')
c.send_keys('123456')
time.sleep(5)
d=driver.find_elements_by_xpath('//*[@class="MuiGrid-root MuiGrid-item"]')
d[3].click()
time.sleep(3)
'''
import datetime,time


def check_date_time_past_data_or_not(driver):
    name = driver.find_element_by_tag_name('title')
    print(name.text)


driver = webdriver.Chrome()
driver.get('https://mkekabet.com/Home/LiveNow')
check_date_time_past_data_or_not(driver)