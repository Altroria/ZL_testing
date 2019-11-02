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


class DepWeixglPage():
    def __init__(self, driver):
        #BaseHandle.__init__(self, driver)
        self.handle = BaseHandle(driver)

    #切换iframe
    def __switch_iframe(self):
        self.handle.switch_iframe("iframe", "iframe_weixgl")

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

    def weix_ss(self, value):
        '''
        维修审核
        value:退回、送审、同意、不同意
        '''
        self.handle.switch_users("部门资产管理员")
        self.handle.click_first_class_menu("维修管理")
        self.__switch_iframe()
        time.sleep(0.5)
        self.handle.click_element("通用", "勾选卡片", 0)
        self.handle.click_element("维修管理", "审核")
        self.handle.switch_iframe()
        self.handle.switch_iframe("iframe", "iframe1")
        time.sleep(0.5)
        self.handle.click_element("通用", value)
        time.sleep(0.5)
        self.handle.click_element("维修管理", "保存")
        if self.__get_message() == "审核成功！":
            return True
        else:
            return False

    def weix_yans(self, key):
        '''
        维修验收
        key:维修费用
        '''
        self.handle.switch_users("部门资产管理员")
        self.handle.click_first_class_menu("维修管理")
        self.__switch_iframe()
        time.sleep(0.5)
        self.handle.click_element("通用", "已审核")
        self.handle.click_element("维修管理", "维修验收")
        self.handle.click_element("维修管理", "选择维修商", 1)
        time.sleep(2)
        self.handle.click_element("维修管理", "勾选维修商")
        self.handle.click_element("维修管理", "选择维修商确定")
        self.handle.send_value("通用", "输入框", key, 2)
        self.handle.click_element("通用", "确定")


if __name__ == "__main__":
    driver = webdriver.Chrome()
    a = DepWeixglPage(driver)
    driver.get('http://58.246.240.154:7878/zl/179001')
    time.sleep(1)
    a.handle.send_value('登录', "username", "ss")
    a.handle.send_value('登录', "password", "123")
    driver.maximize_window()
    time.sleep(1)
    a.handle.click_element('登录', 'login')
    time.sleep(5)
    print(a.weix_ss("同意"))
