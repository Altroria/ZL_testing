#coding=utf-8
'''
验收页面
'''

import sys
import os
sys.path.append(os.path.join(os.getcwd()))
from selenium import webdriver

import time
from base.base_handle import BaseHandle


class UserYansPage():
    def __init__(self, driver):
        #BaseHandle.__init__(self, driver)
        self.handle = BaseHandle(driver)

    #切换iframe
    def __switch_iframe(self):
        self.handle.switch_iframe("iframe", "iframe_yansgl")

    def yans_tj(self):
        '''
        验收提交
        '''
        self.handle.switch_users("使用人")
        self.handle.click_first_class_menu("验收资产")
        self.__switch_iframe()
        time.sleep(0.5)
        self.handle.click_element("通用", "勾选卡片", 0)
        self.handle.click_element("验收资产", "提交")


if __name__ == "__main__":
    driver = webdriver.Chrome()
    a = UserYansPage(driver)
    driver.get('http://58.246.240.154:7878/zl/179001')
    time.sleep(1)
    a.handle.send_value('登录', "username", "ss")
    a.handle.send_value('登录', "password", "123")
    driver.maximize_window()
    time.sleep(1)
    a.handle.click_element('登录', 'login')
    time.sleep(5)
    a.yans_tj()
