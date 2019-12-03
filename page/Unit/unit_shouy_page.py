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
        self.handle = BaseHandle(driver)

    #切换iframe
    def switch_iframe(self):
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

    def get_message(self):
        try:
            self.handle.switch_iframe()
            self.handle.wait_element('message', 'message')
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
            message_text = self.handle.get_element("首页", "使用状态").text
        except:
            message_text = None
        return message_text[-4:-1]

    #获取价值
    @BaseHandle.functional_combination("单位资产管理员", "首页", "所有资产")
    def get_jiaz(self):
        try:
            time.sleep(2)
            message_text = self.handle.get_element("首页", "价值").text
        except:
            message_text = None
        return message_text

    #首页发起业务
    @BaseHandle.functional_combination("单位资产管理员", "首页", "所有资产", index=[1])
    def apply_business(self, yewu):
        '''
        打开菜单--->选择卡片--->办理业务
        yewu:业务名称
        '''
        self.handle.click_element("通用", "办理业务")
        self.handle.click_element("首页", yewu)
        time.sleep(1)
        self.handle.click_element("通用", "确定")
        if yewu == "申请出租" or yewu == "申请出借":
            time.sleep(2)
            self.handle.click_element("通用", "确定")

    #申请报修错误
    def apply_weix_error(self):
        self.apply_business("申请报修")
        zt = self.get_shiyzt()
        if self.get_message_error() == zt:
            return True
        else:
            return False

    #操作栏点击申请报修
    @BaseHandle.functional_combination("单位资产管理员", "首页", "所有资产")
    def apply_business_02(self, yewu):
        self.handle.click_level_element("通用", "data_img", "首页", yewu, 0)
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
    @BaseHandle.functional_combination("单位资产管理员", "首页", "待收货", index=[1])
    def receipt(self, value):
        '''
        收货
        value:确认收货、取消收货、全部收货
        '''
        self.handle.click_element("待收货", value)
        time.sleep(0.5)
        if value != "全部收货":
            self.handle.click_element("通用", "确定")

    #申请报修成功
    def repair(self):
        self.handle.apply_business("申请报修")
        if self.__get_suoyzc_message(
        ) == "您选择的卡片已放入“我要报修/维修管理”中，您如果想现在就去提交，请选择“是”;您如果还想继续选择其他卡片，请选择“否”。":
            return True
        else:
            return False

    #申请转移成功
    def transfer(self):
        self.handle.apply_business("申请转移")
        if self.__get_suoyzc_message(
        ) == "您选择的卡片已放入“我要转移/待转移”中，您如果想现在就去提交，请选择“是”；您如果还想继续选择其他卡片，请选择“否”。":
            return True
        else:
            return False

    #申请处置成功
    def management(self):
        self.handle.apply_business("申请处置")
        if self.__get_suoyzc_message(
        ) == "您选择的卡片已放入“我要处置/资产处置”中，您如果想现在就去提交，请选择“是”；您如果还想继续选择其他卡片，请选择“否”。":
            return True
        else:
            return False

    #申请更正成功
    def corrections(self):
        self.handle.apply_business("申请更正")
        if self.__get_suoyzc_message(
        ) == "您选择的卡片已放入信息更正待提交中，您如果想现在就去提交，请选择“是”；您如果还想继续选择其他卡片，请选择“否”。":
            return True
        else:
            return False

    #申请出租成功
    def lease(self):
        self.handle.apply_business("申请出租")
        if self.__get_suoyzc_message(
        ) == "您选择的卡片已放入出租（借）待审核中，您如果想现在就去提交，请选择“是”；您如果还想继续选择其他卡片，请选择“否”。":
            return True
        else:
            return False

    #申请对外投资成功
    def investment(self):
        self.handle.apply_business("申请对外投资")
        if self.__get_suoyzc_message(
        ) == "您选择的卡片已放入对外投资待审核中，您如果想现在就去提交，请选择“是”；您如果还想继续选择其他卡片，请选择“否”。":
            return True
        else:
            return False

    #确认收货成功
    def receipt_success(self):
        '''
        收货
        value:确认收货、取消收货、全部收货
        '''
        self.receipt("确认收货")
        if self.get_message() == "收货成功":
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
    a = ShouyPage(driver)
    driver.get('http://58.246.240.154:7878/zl/179333')
    a.handle.send_value('登录', "username", "ss")
    a.handle.send_value('登录', "password", "123")
    time.sleep(1)
    a.handle.click_element('登录', 'login')
    time.sleep(5)
    a.apply_business("申请转移")
