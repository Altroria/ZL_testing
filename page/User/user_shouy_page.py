#coding=utf-8
'''
使用人首页
'''

import sys
import os
sys.path.append(os.path.join(os.getcwd()))
from selenium import webdriver

import time
from base.base_handle import BaseHandle


class UserShouyPage():
    def __init__(self, driver):
        self.driver = driver
        self.handle = BaseHandle(driver)

    #切换iframe
    def switch_iframe(self):
        self.handle.switch_iframe("iframe", "iframe_home")

    #获取成功发起流程信息
    def __get_message(self):
        try:
            self.handle.switch_iframe()
            time.sleep(0.5)
            message_text = self.handle.get_element('message', 'message').text
        except:
            message_text = None
        return message_text

    #获取流程中卡片发起业务，提示信息
    def get_message_error(self):
        try:
            time.sleep(3)
            message_text = self.handle.get_element('message',
                                                   'ty_message').text
        except:
            message_text = None
        return message_text[-5:-2]

    #获取使用状态
    def get_shiyzt(self):
        try:
            time.sleep(2)
            message_text = self.handle.get_element("使用人_首页", "使用状态").text
        except:
            message_text = None
        return message_text[-4:-1]

    #获取价值
    @BaseHandle.functional_combination("使用人", "首页", "所有资产")
    def get_jiaz(self):
        try:
            time.sleep(2)
            message_text = self.handle.get_element("使用人_首页", "价值").text
        except:
            message_text = None
        return message_text

    #打开菜单--->选择卡片--->办理业务
    @BaseHandle.functional_combination("使用人", "首页", "所有资产", index=[1])
    def apply_business(self, yewu):
        '''
        选择卡片--->办理业务
        yewu:申请转移、申请归还、申请报修、申请处置
        '''
        self.handle.click_element("使用人_首页", yewu)
        time.sleep(1)
        self.handle.click_element("通用", "确定")
        if yewu == "申请归还":
            time.sleep(2)
            self.handle.click_element("使用人_首页", "确定")
        time.sleep(2)

    #申请报修错误
    def apply_weix_error(self):
        self.apply_business("申请报修")
        zt = self.get_shiyzt()
        if self.get_message_error() == zt:
            return True
        else:
            return False

    #操作栏点击申请报修
    @BaseHandle.functional_combination("使用人", "首页", "所有资产")
    def apply_business_02(self, yewu):
        self.handle.click_level_element("通用", "data_img", "使用人_首页", yewu, 0)
        time.sleep(1)
        self.handle.click_element("通用", "确定")
        if yewu == "申请归还":
            time.sleep(2)
            self.handle.click_element("使用人_首页", "确定")

    #物品操作——申请成功
    def apply_business_success(self, value):
        self.apply_business_02(value)
        self.handle.wait_element("通用", "否")
        self.handle.click_element("通用", "否")
        time.sleep(2)
        if value == "操作_申请报修" and self.get_shiyzt() == "维修中":
            return True
        elif value == "操作_申请转移" and self.get_shiyzt() == "转移中":
            return True
        elif value == "操作_申请处置" and self.get_shiyzt() == "处置中":
            return True
        else:
            return False

    #收货
    @BaseHandle.functional_combination("使用人", "首页", "待收货", index=[1])
    def receipt(self, value):
        '''
        收货
        value:确认收货、取消收货、全部收货
        '''
        self.handle.click_element("待收货", value)
        time.sleep(0.5)
        if value != "全部收货":
            self.handle.click_element("通用", "确定")

    #确认收货成功
    def receipt_success(self, value):
        '''
        收货
        value:确认收货、取消收货、全部收货
        '''
        self.receipt("确认收货")
        if self.__get_message() == "收货成功":
            return True
        else:
            return False

    #取消收货成功
    def cancel_receipt_success(self):
        '''
        取消收货
        '''
        self.receipt("取消收货")
        if self.get_message() == "取消收货成功":
            return True
        else:
            return False

    #全部收货成功
    def all_receipt_success(self):
        '''
        全部收货
        '''
        self.receipt("全部收货")
        if self.get_message() == "收货成功":
            return True
        else:
            return False


if __name__ == "__main__":
    driver = webdriver.Chrome()
    a = UserShouyPage(driver)
    driver.get('http://58.246.240.154:7878/zl/179333')
    a.handle.send_value('登录', "username", "ss")
    a.handle.send_value('登录', "password", "123")
    time.sleep(1)
    a.handle.click_element('登录', 'login')
    time.sleep(1)
    print(a.get_jiaz())
