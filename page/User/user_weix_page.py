#coding=utf-8
'''
资产维修页面
'''

import sys
import os
sys.path.append(os.path.join(os.getcwd()))
from selenium import webdriver

import time
from base.base_handle import BaseHandle


class UserWeixPage():
    def __init__(self, driver):
        self.handle = BaseHandle(driver)

    #切换iframe
    def __switch_iframe(self):
        self.handle.switch_iframe("iframe", "iframe_weixgl")

    @BaseHandle.functional_combination("使用人", "我要报修", index=[1])
    def weix_ss(self, value):
        '''
        维修
        value:删除申请、提交申请
        '''
        self.handle.click_element("我要报修", value)
        self.handle.click_element("通用", "确定")

    @BaseHandle.functional_combination("使用人", "我要报修", "已审核")
    def weix_yans(self, key):
        '''
        维修验收
        key:维修费用
        '''
        self.handle.click_element("维修管理", "维修验收")
        time.sleep(2)
        self.handle.click_element("维修管理", "选择维修商", 1)
        time.sleep(2)
        self.handle.click_element("维修管理", "勾选维修商")
        self.handle.click_element("维修管理", "选择维修商确定")
        self.handle.send_value("通用", "输入框", key, 2)
        self.handle.click_element("通用", "确定")


if __name__ == "__main__":
    driver = webdriver.Chrome()
    a = UserWeixPage(driver)
    driver.get('http://58.246.240.154:7878/zl/6666')
    time.sleep(1)
    a.send_value('登录', "username", "ss")
    a.send_value('登录', "password", "123")
    driver.maximize_window()
    time.sleep(1)
    a.click_element('登录', 'login')
    time.sleep(5)
    a.weix_yans(100)
