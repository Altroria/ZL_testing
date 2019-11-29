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
        self.handle = BaseHandle(driver)

    #切换iframe
    def switch_iframe(self):
        self.handle.switch_iframe("iframe", "iframe_peizgl")

    #获取提示信息
    def __get_message(self):
        try:
            time.sleep(1)
            self.handle.switch_iframe()
            message_text = self.handle.get_element('message',
                                                   'ty_message').text
        except:
            message_text = None
        return message_text

    #单位审核
    @BaseHandle.functional_combination("单位资产管理员", "配置管理", index=[1])
    def peiz_ss(self, value):
        '''
        单位审核
        value:退回、同意、不同意
        '''
        self.handle.click_element("配置管理", "审核")
        self.handle.switch_iframe()
        self.handle.switch_iframe("iframe", "iframe1")
        self.handle.click_element("通用", value)
        time.sleep(1)
        self.handle.click_element("配置管理", "保存")

    #单位审核成功
    def peiz_ss_success(self, value):
        '''
        单位审核
        value:退回、同意、不同意
        '''
        self.peiz_ss(value)
        if self.__get_message() == "审核成功！":
            return True
        else:
            return False

    def peiz_ss_tuih(self):
        '''
        单位审核退回
        '''
        self.peiz_ss("退回")
        if self.__get_message() == "审核成功！":
            return True
        else:
            return False


if __name__ == "__main__":
    driver = webdriver.Chrome()
    a = PeizlPage(driver)
    driver.get('http://58.246.240.154:7878/zl/179333')
    time.sleep(1)
    a.handle.send_value('登录', "username", "ss")
    a.handle.send_value('登录', "password", "123")
    driver.maximize_window()
    time.sleep(1)
    a.handle.click_element('登录', 'login')
    time.sleep(2)
    print(a.peiz_ss_success("退回"))
