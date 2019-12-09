#coding=utf-8
'''
资产维修
'''

import sys
import os
sys.path.append(os.path.join(os.getcwd()))
from selenium import webdriver

import time
from base.base_handle import BaseHandle


class FinWeixPage():
    def __init__(self, driver):
        self.handle = BaseHandle(driver)

    #切换iframe
    def switch_iframe(self):
        self.handle.switch_iframe("iframe", "iframe_weixgl")

    #获取提示信息
    def __get_message(self):
        try:
            self.handle.switch_iframe()
            self.handle.wait_element('message', 'message')
            message_text = self.handle.get_element('message', 'message').text
        except:
            message_text = None
        return message_text

    @BaseHandle.functional_combination("财务制单人员", "资产修理", index=[1])
    def weix_dengz(self, value):
        '''
        维修费用化登账
        value:资本化 or 费用化
        '''
        self.handle.click_element("通用", "登账")
        self.handle.click_element("财务_资产修理", value)
        time.sleep(1)
        self.handle.click_element("财务_资产修理", "财务入账日期", 0)
        time.sleep(1)
        self.handle.click_element("通用", "今天")
        self.handle.send_value("通用", "输入框", 1000, 3)
        jiaz = self.handle.get_element("财务_资产修理", "价值").text
        self.handle.send_value("通用", "输入框", jiaz, 4)  # 财政补助收入
        if value == "资本化":
            self.handle.send_value("通用", "输入框", 10, 7)  # 重新设置剩余折旧年限
        time.sleep(1)
        self.handle.click_element("财务_资产修理", "登账", 1)

    def weix_dengz_success(self, value):
        '''
        维修费用化登账
        value:资本化 or 费用化
        '''
        self.weix_dengz(value)
        if value == "费用化" and self.__get_message() == "费用化登账成功":
            return True
        elif value == "资本化" and self.__get_message() == "资本化登账成功":
            return True
        else:
            return False


if __name__ == "__main__":
    driver = webdriver.Chrome()
    a = FinWeixPage(driver)
    driver.get('http://58.246.240.154:7878/zl/179333')
    a.handle.send_value('登录', "username", "ss")
    a.handle.send_value('登录', "password", "123")
    time.sleep(1)
    a.handle.click_element('登录', 'login')
    print(a.weix_dengz_success("费用化"))
