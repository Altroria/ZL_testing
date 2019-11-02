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
        #BaseHandle.__init__(self, driver)
        self.handle = BaseHandle(driver)

    #切换iframe
    def __switch_iframe_guih(self):
        #self.handle.switch_iframe("iframe", "iframe_zicgh")
        self.handle.switch_iframe("iframe", "iframe_guih")

    def guih_pass(self):
        '''
        归还
        '''
        self.handle.switch_users("使用人")
        self.handle.click_two_level_menu("资产归还")
        self.__switch_iframe_guih()
        time.sleep(0.5)
        self.handle.click_element("通用", "勾选卡片", 0)
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
