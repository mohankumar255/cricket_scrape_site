import datetime
from win10toast import ToastNotifier
from logging import *
import time


def disable_footer_notification(driver):
    try:
        # disable_notification_close_id_tag
        close_button_id_tag = driver.find_element_by_id('dengage-push-perm-banner')
        # close button class name
        close_button_class_tag = close_button_id_tag.find_element_by_class_name(
            'dn-banner-deny-btn')
        close_button_class_tag.click()
        # message = 'disbled footer notification '
        time.sleep(2)
    except Exception as error:
        print(error)
        pass


def disbale_header_notification(driver):
    try:
        # notification close button class tag
        colse_btn_class_tag = driver.find_element_by_class_name("dn-slide-deny-btn")
        colse_btn_class_tag.click()
        # message = 'disabled header notification'
        time.sleep(5)
    except Exception as error:
        print(error)
        pass

def notification(message):
    notification=ToastNotifier()
    notification.show_toast('fsb_sites',message)


def log_file(message):
    date=time.strftime('%y-%m-%d')
    file1=open('sample.txt','a')
    file1.write(date+message)
    file1.write('\n')
    file1.close()
    file_name=f'Fsb_Sites_checks/fsb_logs/{date}.log'
    file=open(file_name,'a')
    Format='%(lineno)s *** %(name)s *** %(asctime)s *** %(message)s'
    basicConfig(filename=file_name,filemode='a',format=Format,level=DEBUG)
    info(message)
