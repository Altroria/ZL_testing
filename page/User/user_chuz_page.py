#coding=utf-8
'''
资产处置页面
'''

import sys
import os
sys.path.append(os.path.join(os.getcwd()))
from selenium import webdriver

import time
from base.base_handle import BaseHandle


class UserZicczPage():
    def __init__(self, driver):
        #BaseHandle.__init__(self, driver)
        self.handle = BaseHandle(driver)

    #切换iframe
    def __switch_iframe_ziccz(self):
        #self.handle.switch_iframe("iframe", "iframe_woycz")
        self.handle.switch_iframe("iframe", "iframe_ziccz")

    #处置提交
    def chuz_ss(self, value):
        '''
        处置提交
        value:提交申请、删除申请
        '''
        self.handle.switch_users("使用人")
        self.handle.click_first_class_menu("我要处置")
        self.__switch_iframe_ziccz()
        self.handle.click_element("通用", "勾选卡片", 0)
        self.handle.click_element("我要处置", value)
        self.handle.click_element("通用", "确定")


if __name__ == "__main__":
    driver = webdriver.Chrome()
    a = UserZicczPage(driver)
    driver.get('http://58.246.240.154:7878/zl/6666')
    driver.maximize_window()
    time.sleep(1)
    a.send_value('登录', "username", "ss")
    a.send_value('登录', "password", "123")
    time.sleep(1)
    a.click_element('登录', 'login')
    time.sleep(2)
    a.chuz_ss("提交申请")
