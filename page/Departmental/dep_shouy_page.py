#coding=utf-8
'''
部门首页
'''

import sys
import os
sys.path.append(os.path.join(os.getcwd()))
from selenium import webdriver

import time
from base.base_handle import BaseHandle


class DepShouyPage():
    '''
    部门首页
    '''

    def __init__(self, driver):
        self.handle = BaseHandle(driver)

    #切换iframe
    def switch_iframe(self):
        self.handle.switch_iframe("iframe", "iframe_home")

    def __get_message(self):
        try:
            self.handle.switch_iframe()
            self.handle.driver.implicitly_wait(3)
            message_text = self.handle.get_element('message', 'message').text
        except:
            message_text = None
        return message_text

    #打开菜单--->选择卡片--->办理业务
    @BaseHandle.functional_combination("部门资产管理员", "首页", "所有资产", index=[1])
    def apply_business(self, yewu):
        '''
        打开菜单--->选择卡片--->办理业务
        yewu:申请报修、申请转移、申请归还、申请处置
        '''
        #self.handle.click_element("首页", "图片列表模式")
        self.handle.click_element("通用", "办理业务")
        self.handle.click_element("首页", yewu)
        time.sleep(1)
        self.handle.click_element("通用", "确定")
        if yewu == "申请归还":
            time.sleep(2)
            self.handle.click_element("使用人_首页", "确定")

    @BaseHandle.functional_combination("部门资产管理员", "首页", "待收货", index=[1])
    def receipt(self, value):
        '''
        确认收货
        value: 确认收货、取消收货、全部收货
        '''
        self.handle.click_element("待收货", "确认收货")
        time.sleep(0.5)
        if value != "全部收货":
            self.handle.click_element("通用", "确定")

    def receipt_success(self):
        self.receipt()
        if self.__get_message() == "收货成功":
            return True
        else:
            return False

    def cancel_receipt_success(self):
        self.receipt("取消收货")
        if self.__get_message() == "取消收货成功":
            return True
        else:
            return False

    def all_receipt_success(self):
        self.receipt("全部收货")
        if self.__get_message() == "收货成功":
            return True
        else:
            return False


if __name__ == "__main__":
    driver = webdriver.Chrome()
    a = DepShouyPage(driver)
    driver.get('http://58.246.240.154:7878/zl/179333')
    a.handle.send_value('登录', "username", "ss")
    a.handle.send_value('登录', "password", "123")
    time.sleep(1)
    a.handle.click_element('登录', 'login')
    time.sleep(1)
    print(a.apply_business("申请转移"))
