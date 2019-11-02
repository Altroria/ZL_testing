#coding=utf-8
'''
单位配置管理
'''

import sys
import os
sys.path.append(os.path.join(os.getcwd()))
from selenium import webdriver

import time
from base.base_handle import BaseHandle


class PeizlPage():
    def __init__(self, driver):
        #BaseHandle.__init__(self, driver)
        self.handle = BaseHandle(driver)

    #切换iframe
    def __switch_iframe(self):
        self.handle.switch_iframe("iframe", "iframe_peizgl")

    #获取提示信息
    def __get_message(self):
        try:
            time.sleep(1)
            self.handle.switch_iframe()
            message_text = self.handle.get_element('message', 'ty_message').text
        except:
            message_text = None
        return message_text

    def peiz_ss(self, value):
        '''
        单位审核
        value:退回、同意、不同意
        '''
        self.handle.switch_users("单位资产管理员")
        self.handle.click_first_class_menu("配置管理")
        self.__switch_iframe()
        time.sleep(0.5)
        self.handle.click_element("通用", "勾选卡片", 0)
        self.handle.click_element("配置管理", "审核")
        self.handle.switch_iframe()
        self.handle.switch_iframe("iframe", "iframe1")
        self.handle.click_element("通用", value)
        self.handle.click_element("配置管理", "保存")
        if self.__get_message() == "审核成功！":
            return True
        else:
            return False


if __name__ == "__main__":
    driver = webdriver.Chrome()
    a = PeizlPage(driver)
    driver.get('http://58.246.240.154:7878/zl/6666')
    time.sleep(1)
    a.send_value('登录', "username", "ss")
    a.send_value('登录', "password", "123")
    driver.maximize_window()
    time.sleep(1)
    a.click_element('登录', 'login')
    time.sleep(2)
    a.peiz_sh_ty()
