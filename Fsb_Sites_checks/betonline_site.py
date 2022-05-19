from selenium import webdriver
import time

driver = webdriver.Chrome()
url = 'https://www.betonline.ag/sportsbook/live-betting'
driver.get(url)
time.sleep(5)
sport_clicks = driver.find_elements_by_tag_name('div')
print('ff')
count = 0
c = driver.find_elements_by_class_name('expGlyph')
for i in c:
    print(c.text)

time.sleep(5)
# sport_click.click()
time.sleep(5)
driver.close()
