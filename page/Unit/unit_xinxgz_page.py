#coding=utf-8
'''
信息更正页面
'''

import sys
import os
sys.path.append(os.path.join(os.getcwd()))
from selenium import webdriver

import time
from base.base_handle import BaseHandle


class XinxgzPage():
    def __init__(self, driver):
        self.driver = driver
        self.handle = BaseHandle(driver)

    #切换iframe
    def switch_iframe(self):
        self.handle.switch_iframe("iframe", "iframe_xinxgz")

    #获取提示信息
    def __get_message(self):
        try:
            self.handle.switch_iframe()
            self.handle.wait_element('message', 'message_shenhcg')
            message_text = self.handle.get_element('message',
                                                   'message_shenhcg').text
        except:
            message_text = None
        return message_text

    @BaseHandle.functional_combination("使用人", "我要处置", [1, 2])
    def weix_ss(self):
        '''
        维修审核
        value:退回、送审、同意、不同意
        '''
        print(1111111111111111)


if __name__ == "__main__":
    driver = webdriver.Chrome()
    a = XinxgzPage(driver)
    driver.get('http://58.246.240.154:7878/zl/179333')
    time.sleep(1)
    a.handle.send_value('登录', "username", "ss")
    a.handle.send_value('登录', "password", "123")
    driver.maximize_window()
    time.sleep(1)
    a.handle.click_element('登录', 'login')
    time.sleep(5)
    a.weix_ss()
