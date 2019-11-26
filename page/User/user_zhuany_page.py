#coding=utf-8
'''
资产转移页面
'''

import sys
import os
sys.path.append(os.path.join(os.getcwd()))
from selenium import webdriver

import time
from base.base_handle import BaseHandle


class UserZhuanyPage():
    def __init__(self, driver):
        self.handle = BaseHandle(driver)

    #切换iframe
    def switch_iframe(self):
        self.handle.switch_iframe("iframe", "iframe_zhuany")

    #转移
    @BaseHandle.functional_combination("使用人", "资产转移", index=[1])
    def zhuany(self, value):
        '''
        转移
        value:使用人、部门
        '''
        self.handle.click_element("资产转移", "办理业务")
        time.sleep(0.5)
        self.handle.click_element("资产转移", "添加接收方", 0)
        time.sleep(0.5)
        if value == "使用人":
            self.handle.click_element("资产转移", "勾选添加接收方")
        self.handle.click_element("通用", "确定")
        time.sleep(0.5)
        self.handle.click_element("通用", "勾选卡片", 0)
        self.handle.click_element("资产转移", "办理业务")
        self.handle.click_element("资产转移", "转移", 0)
        time.sleep(1)
        self.handle.click_element("通用", "确定")


if __name__ == "__main__":
    driver = webdriver.Chrome()
    a = UserZhuanyPage(driver)
    driver.get('http://58.246.240.154:7878/zl/179333')
    a.handle.send_value('登录', "username", "ss")
    a.handle.send_value('登录', "password", "123")
    time.sleep(1)
    a.handle.click_element('登录', 'login')
    time.sleep(1)
    a.zhuany("使用人")
