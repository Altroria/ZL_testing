#coding=utf-8
'''
资产处置页面
'''

import sys
import os
sys.path.append(os.path.join(os.getcwd()))
from selenium import webdriver

import time
from base.base_handle import BaseHandle


class ZicczPage():
    def __init__(self, driver):
        #Base__init__(self, driver)
        self.handle = BaseHandle(driver)

    #切换iframe
    def __switch_iframe(self):
        self.handle.switch_iframe("iframe", "iframe_ziccz")

    #获取提示信息
    def __get_message(self):
        try:
            self.handle.switch_iframe()
            self.handle.wait_element('message', 'message')
            message_text = self.handle.get_element('message', 'message').text
        except:
            message_text = None
        return message_text

    #处置审核通过
    def chuz_shengcczd(self):
        '''
        处置生成处置单
        '''
        self.handle.switch_users("单位资产管理员")
        self.handle.click_first_class_menu("资产处置")
        self.__switch_iframe()
        self.handle.click_element("通用", "勾选卡片", 0)
        self.handle.click_element("资产处置", "生成处置申请单")
        time.sleep(2)
        self.handle.click_element("通用", "勾选卡片", 0)
        self.handle.click_element("资产处置", "下一步")
        time.sleep(1)
        self.handle.send_value("通用", "输入框", 1000, 0)
        while self.handle.get_element("通用", "确定") == None:
            try:
                self.handle.click_element("资产处置", "下一步", 0)
            except:
                continue
        self.handle.click_element("通用", "确定")
        time.sleep(2)
        self.handle.send_value("通用", "输入框", 1, 1)
        self.handle.send_value("通用", "输入框", 2, 2)
        self.handle.send_value("通用", "输入框", 3, 3)
        self.handle.send_value("通用", "输入框", 4, 4)
        self.handle.send_value("通用", "输入框", 5, 5)
        self.handle.send_value("通用", "输入框", 6, 7)
        self.handle.click_element("资产处置", "附报材料")
        time.sleep(1)
        self.handle.click_element("资产处置", "附报材料_勾选", 0)
        self.handle.click_element("资产处置", "附报材料_勾选", 1)
        self.handle.click_element("资产处置", "附报材料_勾选", 4)
        self.handle.click_element("资产处置", "下一步")

    #待审核送审
    def chuz_songs(self):
        '''
        待审核送审
        '''
        self.handle.switch_users("单位资产管理员")
        self.handle.click_first_class_menu("资产处置")
        self.__switch_iframe()
        self.handle.click_element("资产处置", "待送审")
        self.handle.click_element("通用", "勾选卡片", 0)
        time.sleep(1)
        self.handle.click_element("资产处置", "送审")
        time.sleep(1)
        self.handle.click_element("通用", "确定")

    #执行处置
    def chuz_zhix(self):
        '''
        执行处置
        '''
        self.handle.switch_users("单位资产管理员")
        self.handle.click_first_class_menu("资产处置")
        self.__switch_iframe()
        self.handle.click_element("资产处置", "已审核")
        self.handle.click_element("资产处置", "执行处置")
        self.handle.click_element("通用", "勾选卡片", 0)
        self.handle.click_element("资产处置", "执行")

    def chuz_chuzhi(self):
        '''
        执行页面，处置流程
        '''
        self.handle.switch_users("单位资产管理员")
        self.handle.click_first_class_menu("资产处置")
        self.__switch_iframe()
        self.handle.click_element("资产处置", "执行中")
        self.handle.click_element("资产处置", "处置流程")
        time.sleep(1)
        self.handle.click_element("资产处置", "添加买受方")
        time.sleep(1)
        self.handle.click_element("通用", "勾选卡片", 0)
        self.handle.click_element("通用", "确定")
        time.sleep(1)
        self.handle.click_element("资产处置", "下一步")
        time.sleep(1)
        self.handle.click_element("通用", "勾选卡片", 0)
        self.handle.click_element("资产处置", "下一步")
        time.sleep(2)
        self.handle.send_value("通用", "输入框", 1, 0)
        self.handle.send_value("通用", "输入框", 2, 1)
        self.handle.click_element("资产处置", "送财务登账")
        if self.handle.get_element("资产处置", "执行处置") == None:
            return True
        else:
            return False


if __name__ == "__main__":
    driver = webdriver.Chrome()
    a = ZicczPage(driver)
    driver.get('http://58.246.240.154:7878/zl/179001')
    a.handle.send_value('登录', "username", "ss")
    a.handle.send_value('登录', "password", "123")
    time.sleep(1)
    a.handle.click_element('登录', 'login')
    time.sleep(1)
    a.chuz_chuzhi()
