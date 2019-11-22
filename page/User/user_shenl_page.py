#coding=utf-8
'''
使用人我要申领
'''

import sys
import os
sys.path.append(os.path.join(os.getcwd()))
from selenium import webdriver

import time
from base.base_handle import BaseHandle


class UserShenllPage():
    def __init__(self, driver):
        self.handle = BaseHandle(driver)

    #切换iframe
    def switch_iframe(self):
        self.handle.switch_iframe("iframe", "iframe_peizgl")

    #增加申领--提交
    @BaseHandle.functional_combination("使用人", "我要申领")
    def shenl_xinz(self, card_value):
        '''
        增加申领--提交
        card_value:分类明细
        '''
        self.handle.click_element("我要申领", "增加申领资产")
        self.handle.switch_iframe()
        self.handle.switch_iframe("iframe", "iframe1")
        time.sleep(2)
        self.handle.choice_first_class(card_value)
        self.handle.click_element("验收管理", "确定")
        time.sleep(2)
        self.handle.switch_iframe()
        self.switch_iframe()
        time.sleep(1)
        self.handle.click_element("通用", "输入框", 6)
        time.sleep(1)
        self.handle.click_element("我要申领", "办公使用")
        self.handle.click_element("通用", "确定")
        time.sleep(1)

    @BaseHandle.functional_combination("使用人", "我要申领", index=[1])
    def shenl_tj(self):
        self.handle.click_element("我要申领", "提交申领")
        self.handle.switch_iframe()


if __name__ == "__main__":
    driver = webdriver.Chrome()
    a = UserShenllPage(driver)
    driver.get('http://58.246.240.154:7878/zl/179107')
    time.sleep(1)
    a.send_value('登录', "username", "ss")
    a.send_value('登录', "password", "123qwe")
    driver.maximize_window()
    time.sleep(1)
    a.click_element('登录', 'login')
    time.sleep(5)
    a.shenl_tj("PC服务器")
