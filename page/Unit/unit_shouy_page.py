#coding=utf-8
'''
所有资产页面
'''

import sys
import os
sys.path.append(os.path.join(os.getcwd()))
from selenium import webdriver

import time
from base.base_handle import BaseHandle


class ShouyPage():
    def __init__(self, driver):
        #Base__init__(self, driver)
        self.handle = BaseHandle(driver)

    #切换iframe
    def __switch_iframe(self):
        self.handle.switch_iframe("iframe", "iframe_home")

    #获取提示信息
    def __get_suoyzc_message(self):
        try:
            self.handle.wait_element_not("message", "提示")
            self.handle.wait_element("message", "信息")
            time.sleep(0.5)
            message_text = self.handle.get_element("message",
                                                   "ty_message").text
        except:
            message_text = None
        return message_text

    def __get_shouh_message(self):
        try:
            self.handle.switch_iframe()
            self.handle.wait_element('message', 'message')
            message_text = self.handle.get_element('message', 'message').text
        except:
            message_text = None
        return message_text

    def apply_business(self, yewu):
        '''
        打开菜单--->选择卡片--->办理业务
        yewu:业务名称
        '''
        self.handle.switch_users("单位资产管理员")
        self.handle.click_first_class_menu("首页")
        self.__switch_iframe()
        self.handle.click_element("首页", "所有资产")
        self.handle.click_element("首页", "图片列表模式")
        '''
        #获取登账、未在业务中的卡片编号
        if yewu != "申请转移":
            zic_value = self.handle.get_card_number()
            self.handle.search_assets(zic_value)
        '''
        self.handle.click_element("通用", "勾选卡片", 0)
        self.handle.click_element("首页", "办理业务")
        self.handle.click_element("首页", yewu)
        time.sleep(1)
        self.handle.click_element("通用", "确定")
        if yewu == "申请出租" or yewu == "申请出借":
            time.sleep(2)
            self.handle.click_element("通用", "确定")

    def repair(self):
        self.handle.apply_business("申请报修")
        if self.__get_suoyzc_message(
        ) == "您选择的卡片已放入“我要报修/维修管理”中，您如果想现在就去提交，请选择“是”;您如果还想继续选择其他卡片，请选择“否”。":
            return True
        else:
            return False

    def transfer(self):
        self.handle.apply_business("申请转移")
        if self.__get_suoyzc_message(
        ) == "您选择的卡片已放入“我要转移/待转移”中，您如果想现在就去提交，请选择“是”；您如果还想继续选择其他卡片，请选择“否”。":
            return True
        else:
            return False

    def management(self):
        self.handle.apply_business("申请处置")
        if self.__get_suoyzc_message(
        ) == "您选择的卡片已放入“我要处置/资产处置”中，您如果想现在就去提交，请选择“是”；您如果还想继续选择其他卡片，请选择“否”。":
            return True
        else:
            return False

    def corrections(self):
        self.handle.apply_business("申请更正")
        if self.__get_suoyzc_message(
        ) == "您选择的卡片已放入信息更正待提交中，您如果想现在就去提交，请选择“是”；您如果还想继续选择其他卡片，请选择“否”。":
            return True
        else:
            return False

    def lease(self):
        self.handle.apply_business("申请出租")
        if self.__get_suoyzc_message(
        ) == "您选择的卡片已放入出租（借）待审核中，您如果想现在就去提交，请选择“是”；您如果还想继续选择其他卡片，请选择“否”。":
            return True
        else:
            return False

    def investment(self):
        self.handle.apply_business("申请对外投资")
        if self.__get_suoyzc_message(
        ) == "您选择的卡片已放入对外投资待审核中，您如果想现在就去提交，请选择“是”；您如果还想继续选择其他卡片，请选择“否”。":
            return True
        else:
            return False

    #确认收货
    def receipt(self):
        '''
        确认收货
        '''
        self.handle.switch_users("单位资产管理员")
        self.handle.click_first_class_menu("首页")
        self.__switch_iframe()
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
        '''
        取消收货
        '''
        self.handle.switch_users("单位资产管理员")
        self.handle.click_first_class_menu("首页")
        self.__switch_iframe()
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
        '''
        全部收货
        '''
        self.handle.switch_users("单位资产管理员")
        self.handle.click_first_class_menu("首页")
        self.__switch_iframe()
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
    a = ShouyPage(driver)
    driver.get('http://58.246.240.154:7878/zl/6666')
    a.send_value('登录', "username", "ss")
    a.send_value('登录', "password", "123")
    time.sleep(1)
    a.click_element('登录', 'login')
    time.sleep(5)
    a.receipt()
