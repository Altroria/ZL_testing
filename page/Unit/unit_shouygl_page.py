#coding=utf-8
'''
收益管理
'''

import sys
import os
sys.path.append(os.path.join(os.getcwd()))
from selenium import webdriver

import time
from base.base_handle import BaseHandle


class ShouyglPage():
    def __init__(self, driver):
        #BaseHandle.__init__(self, driver)
        self.handle = BaseHandle(driver)

    #切换iframe
    def switch_iframe(self):
        self.handle.switch_iframe("iframe", "iframe_shouygl")

    @BaseHandle.functional_combination("单位资产管理员", "收益管理", index=[1])
    def shouy_ss(self):
        '''
        收益送财务
        '''
        self.handle.click_element("收益管理", "送财务登账")
        self.handle.click_element("通用", "确定")


if __name__ == "__main__":
    driver = webdriver.Chrome()
    a = ShouyglPage(driver)
    driver.get('http://58.246.240.154:7878/zl/179001')
    a.handle.send_value('登录', "username", "ss")
    a.handle.send_value('登录', "password", "123")
    time.sleep(1)
    a.handle.click_element('登录', 'login')
    print(a.shouy_ss())
