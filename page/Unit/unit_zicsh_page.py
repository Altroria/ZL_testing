#coding=utf-8
'''
资产收回页面
'''

import sys
import os
sys.path.append(os.path.join(os.getcwd()))
from selenium import webdriver

import time
from base.base_handle import BaseHandle


class ZicshPage():
    def __init__(self, driver):
        #BaseHandle.__init__(self, driver)
        self.handle = BaseHandle(driver)

    #切换iframe
    def __switch_iframe_zicsh(self):
        #self.handle.switch_iframe("iframe", "iframe_zicsh")
        self.handle.switch_iframe("iframe", "iframe_shouh")

    #获取提示信息
    def __get_zicsh_pass_message(self):
        try:
            self.handle.switch_iframe()
            time.sleep(0.5)
            message_text = self.handle.get_element('message', 'message').text
        except:
            message_text = None
        return message_text

    def take_back(self):
        '''
        收回
        '''
        self.handle.switch_users("单位资产管理员")
        self.handle.click_two_level_menu("资产收回")
        self.__switch_iframe_zicsh()
        time.sleep(0.5)
        self.handle.click_element("资产收回", "操作_收回")
        time.sleep(1)
        self.handle.click_element("通用", "确定")
        if self.__get_zicsh_pass_message() == "收回成功":
            return True
        else:
            return False

    def all_take_back(self):
        '''
        全部收回
        '''
        self.handle.switch_users("单位资产管理员")
        self.handle.click_two_level_menu("资产收回")
        self.__switch_iframe_zicsh()
        time.sleep(0.5)
        self.handle.click_element("通用", "全选")
        self.handle.click_element("资产收回", "收回")
        time.sleep(0.5)
        self.handle.click_element("通用", "确定")
        time.sleep(0.5)
        self.handle.click_element("资产收回", "全部收回确定")
        if self.__get_zicsh_pass_message() == "收回成功":
            return True
        else:
            return False


if __name__ == "__main__":
    driver = webdriver.Chrome()
    a = ZicshPage(driver)
    driver.get('http://58.246.240.154:7878/zl/179333')
    a.handle.send_value('登录', "username", "ss")
    a.handle.send_value('登录', "password", "123")
    time.sleep(1)
    a.handle.click_element('登录', 'login')
    time.sleep(1)
    print(a.all_take_back())
