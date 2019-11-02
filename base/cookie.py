#coding=utf-8
import sys
import os
import time
sys.path.append(os.path.join(os.getcwd()))
from base.base_class import SeleniumDriver
from selenium import webdriver

#driver = BrowserEngine().init_driver()
driver = webdriver.Chrome()
a = SeleniumDriver(driver)
'''
driver.get('http://58.246.240.154:7878/zl/6666')
driver.find_element_by_name("zhanghm").send_keys("ss")
driver.find_element_by_name("psw").send_keys("123")
driver.find_element_by_class_name("login_btn").click()
time.sleep(2)
with open("C:\Automated_testing\ZL_testing\config\login_url.py", 'w') as fp:
    fp.write(json.dumps("danw" + "=" + driver.current_url) + '\n')
'''
driver.get('http://58.246.240.154:7878/zl/6666')
a.set_cookie()
time.sleep(1)
driver.get(
    "http://58.246.240.154:7878/zl/orgHome/index/389F71165DF445CDA125150AFBF331F0/0"
)
try:
    time.sleep(3)
    message_text = a.get_element('通用', 'users').text
except:
    driver.get('http://58.246.240.154:7878/zl/6666')
    driver.find_element_by_name("zhanghm").send_keys("ss")
    driver.find_element_by_name("psw").send_keys("123")
    driver.find_element_by_class_name("login_btn").click()
    time.sleep(2)
    a.get_cookie()
