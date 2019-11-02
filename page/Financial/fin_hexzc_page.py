#coding=utf-8
'''
核销资产
'''

import sys
import os
sys.path.append(os.path.join(os.getcwd()))
from selenium import webdriver

import time
from base.base_handle import BaseHandle


class HexzcPage():
    def __init__(self, driver):
        #BaseHandle.__init__(self, driver)
        self.handle = BaseHandle(driver)

    #切换iframe
    def __switch_iframe(self):
        self.handle.switch_iframe("iframe", "iframe_hexzc")

    def hex_dengz(self):
        '''
        核销登账
        '''
        self.handle.switch_users("财务制单人员")
        self.handle.click_first_class_menu("核销资产")
        self.__switch_iframe()
        sbdh = self.handle.get_elements("财务_核销资产", "申报单号")[0].text
        self.handle.click_element("通用", "勾选卡片", 0)
        self.handle.click_element("财务_核销资产", "登账")
        self.handle.click_element("财务_核销资产", "财务入账日期")
        self.handle.click_element("通用", "今天")
        self.handle.send_value("通用", "输入框", 1000, 1)
        self.handle.click_element("通用", "确定")
        time.sleep(1)
        try:
            new_sbdh = self.handle.get_elements("财务_核销资产", "申报单号")[0].text
            if new_sbdh != sbdh:
                return True
            else:
                return False
        except:
            return True


if __name__ == "__main__":
    driver = webdriver.Chrome()
    a = HexzcPage(driver)
    driver.get('http://58.246.240.154:7878/zl/6666')
    a.send_value('登录', "username", "ss")
    a.send_value('登录', "password", "123")
    time.sleep(1)
    a.click_element('登录', 'login')
    print(a.hex_dengz())
