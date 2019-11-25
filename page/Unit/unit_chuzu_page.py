#coding=utf-8
'''
出租页面
'''

import sys
import os
sys.path.append(os.path.join(os.getcwd()))
from selenium import webdriver

import time
from base.base_handle import BaseHandle


class ChuzPage():
    def __init__(self, driver):
        self.handle = BaseHandle(driver)

    #切换iframe
    def switch_iframe(self):
        self.handle.switch_iframe("iframe", "iframe_zuj")

    #获取提示
    def __get_message(self):
        try:
            self.handle.switch_iframe()
            self.handle.wait_element('message', 'ty_message')
            message_text = self.handle.get_element('message',
                                                   'ty_message').text
        except:
            message_text = None
        return message_text

    #出租生成单据
    @BaseHandle.functional_combination("单位资产管理员", "出租 (借)", index=[1])
    def chuzu_scdj(self):
        '''
        出租生成单据
        '''
        self.handle.click_element("出租", "生成单据")
        self.handle.wait_element("出租", "下一步")
        self.handle.click_element("出租", "下一步")
        time.sleep(1)
        self.handle.click_element("出租", "下一步")
        time.sleep(1)
        self.handle.click_element("出租", "添加承租(借)方")
        self.handle.send_value("通用", "输入框", 1, 1)
        self.handle.send_value("通用", "输入框", 2, 7)
        self.handle.click_element("通用", "确定")
        time.sleep(1)
        self.handle.click_element("出租", "下一步")
        time.sleep(1)
        self.handle.send_value("通用", "输入框", 1, 0)
        self.handle.send_value("通用", "输入框", 2, 1)
        self.handle.send_value("通用", "输入框", 3, 2)
        self.handle.send_value("通用", "输入框", 4, 3)
        self.handle.send_value("通用", "输入框", 5, 4)
        self.handle.send_value("通用", "输入框", 6, 5)
        self.handle.click_element("出租", "附报材料")
        time.sleep(1)
        self.handle.click_element("出租", "附报材料_勾选", 0)
        self.handle.click_element("出租", "附报材料_勾选", 1)
        self.handle.click_element("出租", "附报材料_勾选", 2)
        self.handle.click_element("通用", "确定")

    #送审
    @BaseHandle.functional_combination("单位资产管理员", "出租 (借)", "待送审", index=[1])
    def chuzu_ss(self):
        '''
        送审
        '''
        self.handle.click_element("出租", "送审")
        time.sleep(1)
        self.handle.click_element("通用", "确定")

    #通过
    @BaseHandle.functional_combination("单位资产管理员", "出租 (借)", "审批中")
    def chuzu_tg(self):
        '''
        通过
        '''
        time.sleep(1)
        self.handle.click_element("出租", "通过", 0)
        time.sleep(1)
        self.handle.click_element("通用", "确定")

    #执行
    @BaseHandle.functional_combination("单位资产管理员", "出租 (借)", "已审批")
    def chuzu_zhix(self):
        '''
        执行
        '''
        self.handle.click_element("出租", "执行出租(借)")
        time.sleep(1)
        self.handle.click_element("通用", "确定")

    #登记收益
    @BaseHandle.functional_combination("单位资产管理员", "出租 (借)", "出租(借)中")
    def chuzu_shouyi(self, value):
        '''
        登记收益
        value:暂存  送财务部门
        '''
        self.handle.click_element("出租", "登记收益", 0)
        time.sleep(1)
        self.handle.click_element("通用", "输入框", 0)
        self.handle.click_element("出租", "今天")
        self.handle.send_value("通用", "输入框", 1000, 1)
        self.handle.click_element("出租", value)

    #收回
    @BaseHandle.functional_combination("单位资产管理员", "出租 (借)", "出租(借)中")
    def chuzu_shouh(self):
        '''
        出租资产收回
        '''
        self.handle.click_element("出租", "提前收回")
        time.sleep(1)
        self.handle.click_element("通用", "确定")

    def chuzu_zhix_success(self):
        '''
        执行
        '''
        self.chuzu_zhix()
        if self.__get_message() == "出租(借)成功":
            return True
        else:
            return False

    def chuzu_shouh_success(self):
        '''
        出租资产收回成功
        '''
        self.chuzu_shouh()
        if self.__get_message() == "收回成功":
            return True
        else:
            return False


if __name__ == "__main__":
    driver = webdriver.Chrome()
    a = ChuzPage(driver)
    driver.get('http://58.246.240.154:7878/zl/179333')
    driver.maximize_window()
    time.sleep(1)
    a.handle.send_value('登录', "username", "ss")
    a.handle.send_value('登录', "password", "123")
    time.sleep(1)
    a.handle.click_element('登录', 'login')
    time.sleep(2)
    print(a.chuzu_shouyi("送财务部门"))
