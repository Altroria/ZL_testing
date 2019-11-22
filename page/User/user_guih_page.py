#coding=utf-8
'''
资产归还页面
'''

import sys
import os
sys.path.append(os.path.join(os.getcwd()))
from selenium import webdriver

import time
from base.base_handle import BaseHandle


class UserGuihPage():
    def __init__(self, driver):
        self.handle = BaseHandle(driver)

    #切换iframe
    def switch_iframe(self):
        self.handle.switch_iframe("iframe", "iframe_guih")

    @BaseHandle.functional_combination("使用人", "资产归还", index=[1])
    def guih_pass(self):
        '''
        归还
        '''
        self.handle.click_element("资产归还", "归还")
        self.handle.click_element("通用", "确定")


if __name__ == "__main__":
    driver = webdriver.Chrome()
    a = UserGuihPage(driver)
    driver.get('http://58.246.240.154:7878/zl/6666')
    time.sleep(1)
    a.send_value('登录', "username", "ss")
    a.send_value('登录', "password", "123")
    driver.maximize_window()
    time.sleep(1)
    a.click_element('登录', 'login')
    time.sleep(5)
    print(a.guih_pass())
