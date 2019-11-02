#coding=utf-8
'''
资产转移页面
'''

import sys
import os
sys.path.append(os.path.join(os.getcwd()))
from selenium import webdriver

import time
from base.base_handle import BaseHandle


class ZiczyPage():
    def __init__(self, driver):
        #BaseHandle.__init__(self, driver)
        self.handle = BaseHandle(driver)

    #切换iframe
    def __switch_iframe_ziczy(self):
        #self.handle.switch_iframe("iframe", "iframe_ziczy")
        self.handle.switch_iframe("iframe", "iframe_zhuany")

    #获取提示信息
    def __get_ziczy_pass_message(self):
        try:
            self.handle.switch_iframe()
            self.handle.wait_element('message', 'message')
            message_text = self.handle.get_element('message', 'message').text
        except:
            message_text = None
        return message_text

    def zhuany(self, value):
        '''
        转移
        value:使用人、部门
        '''
        self.handle.switch_users("单位资产管理员")
        self.handle.click_two_level_menu("资产转移")
        self.__switch_iframe_ziczy()
        zicbh = self.handle.get_level_element("通用", "data_info", "通用", "资产编号", 0)
        time.sleep(0.5)
        self.handle.click_element("通用", "勾选卡片", 0)
        time.sleep(0.5)
        self.handle.click_element("资产转移", "办理业务")
        time.sleep(0.5)
        self.handle.click_element("资产转移", "添加接收方")
        time.sleep(0.5)
        if value == "使用人":
            self.handle.click_element("资产转移", "勾选添加接收方")
        time.sleep(0.5)
        self.handle.click_element("通用", "确定")
        time.sleep(1)
        self.handle.click_element("通用", "勾选卡片", 0)
        self.handle.click_element("资产转移", "办理业务")
        self.handle.click_element("资产转移", "转移", 0)
        time.sleep(1)
        self.handle.click_element("通用", "确定")
        time.sleep(1)
        element = self.handle.get_level_element("通用", "data_info", "通用", "资产编号", 0)
        if element == None:
            return True
        else:
            zicbh_new = element.text
            if zicbh_new != zicbh:
                return True
            else:
                return False


if __name__ == "__main__":
    driver = webdriver.Chrome()
    a = ZiczyPage(driver)
    driver.get('http://58.246.240.154:7878/zl/6666')
    a.send_value('登录', "username", "ss")
    a.send_value('登录', "password", "123")
    time.sleep(1)
    a.click_element('登录', 'login')
    time.sleep(1)
    print(a.zhuany("部门"))
