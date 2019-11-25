#coding=utf-8
'''
新增资产业务层
'''

import sys
import os
sys.path.append(os.path.join(os.getcwd()))
from selenium import webdriver

import time
from base.base_handle import BaseHandle


class XinzzcPage():
    def __init__(self, driver):
        #BaseHandle.__init__(self, driver)
        self.handle = BaseHandle(driver)

    #切换iframe
    def switch_iframe(self):
        self.handle.switch_iframe("iframe", "iframe_dengzgl")

    #获取登账卡片编号
    def __get_card_number(self):
        try:
            self.handle.click_first_class_menu("新增资产")
            self.switch_iframe()
            self.handle.click_element("财务_新增资产", "摘要", 0)
            time.sleep(1)
            self.handle.switch_iframe1()
            return self.handle.get_element("财务_新增资产", "资产编号").text
        except:
            return None

    #获取提示信息
    def get_message(self):
        try:
            self.handle.switch_iframe()
            self.handle.driver.implicitly_wait(1)
            message_text = self.handle.get_element('message', '退回成功').text
        except:
            message_text = None
        return message_text

    @BaseHandle.functional_combination("财务制单人员", "新增资产", "待登账", index=[1])
    def dengz(self):
        '''
        财务登账
        '''
        time.sleep(2)
        self.handle.click_element("财务_新增资产", "登账")
        self.handle.switch_iframe1()
        time.sleep(1)
        self.handle.click_element("财务_新增资产", "财务入账日期", 0)
        self.handle.click_element("通用", "今天")
        self.handle.send_value("财务_新增资产", "会计凭证号", 1000)
        self.handle.send_value("财务_新增资产", "发票号", 1000)
        time.sleep(1)
        self.handle.click_element("财务_新增资产", "确认登账")
        self.handle.refresh_f5()

    @BaseHandle.functional_combination("财务制单人员", "新增资产", "待登账", index=[1])
    def tuih(self):
        '''
        财务登账退回
        '''
        self.handle.click_element("财务_新增资产", "退回", 0)
        time.sleep(1)
        self.handle.click_element("通用", "确定")
        time.sleep(1)
        self.handle.click_element("财务_新增资产", "确定")
        self.handle.refresh_f5()

    @BaseHandle.functional_combination("财务制单人员", "新增资产", "待登账", index=[1])
    def dengz_success(self):
        '''
        财务登账成功
        '''
        self.handle.click_element("财务_新增资产", "登账")
        self.handle.switch_iframe1()
        time.sleep(2)
        zibh = self.handle.get_element("财务_新增资产", "资产编号_01").text

        self.handle.refresh_f5()
        self.dengz()
        self.handle.refresh_f5()
        new_zibh = self.__get_card_number()
        if new_zibh != zibh:
            return True
        else:
            return False

    def tuih_success(self):
        '''
        财务登账退回成功
        '''
        self.handle.switch_users("财务制单人员")
        zibh = self.__get_card_number()
        self.handle.refresh_f5()
        self.handle.click_first_class_menu("新增资产")
        self.tuih()
        new_zibh = self.__get_card_number()
        if new_zibh != zibh:
            return True
        else:
            return False


if __name__ == "__main__":
    driver = webdriver.Chrome()
    a = XinzzcPage(driver)
    driver.get('http://58.246.240.154:7878/zl/179333')
    a.handle.send_value('登录', "username", "ss")
    a.handle.send_value('登录', "password", "123")
    time.sleep(2)
    a.handle.click_element('登录', 'login')
    driver.maximize_window()
    a.dengz_success()
