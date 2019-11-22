#coding=utf-8
'''
收益管理
'''

import sys
import os
sys.path.append(os.path.join(os.getcwd()))
from selenium import webdriver

import time
from base.base_handle import BaseHandle


class ShouyiPage():
    def __init__(self, driver):
        self.handle = BaseHandle(driver)

    #切换iframe
    def switch_iframe(self):
        self.handle.switch_iframe("iframe", "iframe_shouygl")

    @BaseHandle.functional_combination("财务制单人员", "收益管理", index=[1])
    def shouy_dengz(self):
        '''
        收益登账
        '''

        self.handle.click_element("通用", "登账")
        self.handle.click_element("财务_收益管理", "财务入账日期")
        self.handle.click_element("财务_收益管理", "今天")
        self.handle.send_value("财务_收益管理", "会计凭证号", 1000)
        self.handle.click_element("财务_收益管理", "登账")
        time.sleep(3)

    def shouy_dengz_success(self):
        sbdh = self.handle.get_elements("财务_收益管理", "申报单号")[0].text
        self.shouy_dengz()
        try:
            new_sbdh = self.handle.get_elements("财务_收益管理", "申报单号")[0].text
            if new_sbdh != sbdh:
                return True
            else:
                return False
        except:
            return True


if __name__ == "__main__":
    driver = webdriver.Chrome()
    a = ShouyiPage(driver)
    driver.get('http://58.246.240.154:7878/zl/179001')
    a.handle.send_value('登录', "username", "ss")
    a.handle.send_value('登录', "password", "123")
    time.sleep(1)
    a.handle.click_element('登录', 'login')
    print(a.shouy_dengz())
