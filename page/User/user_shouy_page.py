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
        #BaseHandle.__init__(self, driver)
        self.handle = BaseHandle(driver)

    #切换iframe
    def __switch_iframe_home(self):
        self.handle.switch_iframe("iframe", "iframe_home")

    def __get_shouh_message(self):
        try:
            self.handle.switch_iframe()
            time.sleep(0.5)
            message_text = self.handle.get_element('message', 'message').text
        except:
            message_text = None
        return message_text

    #打开菜单--->选择卡片--->办理业务
    def apply_business(self, yewu):
        '''
        选择卡片--->办理业务
        yewu:申请转移、申请归还、申请报修、申请处置
        '''
        self.handle.switch_users("使用人")
        self.handle.click_first_class_menu("首页")
        self.__switch_iframe_home()
        self.handle.click_element("首页", "所有资产")
        self.handle.click_element("首页", "图片列表模式")
        '''
        if yewu != "申请转移":
            #获取登账、未在业务中的卡片编号
            zic_value = self.handle.get_card_number("使用人")
            self.handle.search_assets(zic_value)
        '''
        self.handle.click_element("通用", "勾选卡片", 0)
        self.handle.click_element("使用人_首页", yewu)
        time.sleep(1)
        self.handle.click_element("通用", "确定")
        if yewu == "申请归还":
            time.sleep(2)
            self.handle.click_element("使用人_首页", "确定")

    def receipt(self):
        '''
        确认收货
        '''
        self.handle.switch_users("使用人")
        self.handle.click_first_class_menu("首页")
        self.__switch_iframe_home()
        self.handle.click_element("待收货", "待收货")
        time.sleep(0.5)
        self.handle.click_element("通用", "勾选卡片", 0)
        self.handle.click_element("待收货", "确认收货")
        time.sleep(0.5)
        self.handle.click_element("通用", "确定")
        if self.__get_shouh_message() == "收货成功":
            return True
        else:
            return False

    #取消收货
    def cancel_receipt(self):
        self.handle.switch_users("使用人")
        self.handle.click_first_class_menu("首页")
        self.__switch_iframe_home()
        self.handle.click_element("待收货", "待收货")
        time.sleep(0.5)
        self.handle.click_element("通用", "勾选卡片", 0)
        self.handle.click_element("待收货", "取消收货")
        time.sleep(0.5)
        self.handle.click_element("通用", "确定")
        if self.__get_shouh_message() == "取消收货成功":
            return True
        else:
            return False

    #全部收货
    def all_receipt(self):
        self.handle.switch_users("使用人")
        self.handle.click_first_class_menu("首页")
        self.__switch_iframe_home()
        self.handle.click_element("待收货", "待收货")
        time.sleep(0.5)
        self.handle.click_element("通用", "勾选卡片", 0)
        self.handle.click_element("待收货", "全部收货")
        if self.__get_shouh_message() == "收货成功":
            return True
        else:
            return False


if __name__ == "__main__":
    driver = webdriver.Chrome()
    a = UserShouyPage(driver)
    driver.get('http://58.246.240.154:7878/zl/6666')
    a.send_value('登录', "username", "ss")
    a.send_value('登录', "password", "123")
    time.sleep(1)
    a.click_element('登录', 'login')
    time.sleep(1)
    print(a.apply_business("申请维修"))
