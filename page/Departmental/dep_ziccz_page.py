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


class DepZicczPage():
    def __init__(self, driver):
        #BaseHandle.__init__(self, driver)
        self.handle = BaseHandle(driver)

    #切换iframe
    def __switch_iframe(self):
        self.handle.switch_iframe("iframe", "iframe_ziccz")

    #获取提示信息
    def __get_message(self):
        try:
            self.handle.switch_iframe()
            self.handle.wait_element('message', 'message_shenhcg')
            message_text = self.handle.get_element('message', 'message_shenhcg').text
        except:
            message_text = None
        return message_text

    def chuz_ss(self, value):
        '''
        处置审核
        value:退回、送审、同意、不同意
        '''
        self.handle.switch_users("部门资产管理员")
        self.handle.click_first_class_menu("资产处置")
        self.__switch_iframe()
        self.handle.click_element("通用", "勾选卡片", 0)
        time.sleep(1)
        self.handle.click_element("资产处置", "审核")
        time.sleep(1)
        self.handle.switch_iframe1()
        self.handle.click_element("通用", value)
        time.sleep(1)
        self.handle.click_element("通用", "保存")
        if self.__get_message() == "审核成功！":
            return True
        else:
            return False


if __name__ == "__main__":
    driver = webdriver.Chrome()
    a = DepZicczPage(driver)
    driver.get('http://58.246.240.154:7878/zl/179001')
    driver.maximize_window()
    time.sleep(1)
    a.handle.send_value('登录', "username", "ss")
    a.handle.send_value('登录', "password", "123")
    time.sleep(1)
    a.handle.click_element('登录', 'login')
    time.sleep(2)
    print(a.chuz_ss("同意"))
