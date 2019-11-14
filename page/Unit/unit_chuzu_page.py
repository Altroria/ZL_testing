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
        #BaseHandle.__init__(self, driver)
        self.handle = BaseHandle(driver)

    #切换iframe
    def __switch_iframe(self):
        #self.handle.switch_iframe("iframe", "iframe_chuzuj")
        self.handle.switch_iframe("iframe", "iframe_zuj")

    #获取提示
    def __get_message(self):
        try:
            self.handle.switch_iframe()
            self.handle.wait_element('message', 'ty_message')
            message_text = self.handle.get_element('message', 'ty_message').text
        except:
            message_text = None
        return message_text

    #出租生成单据
    def chuzu_scdj(self):
        '''
        出租生成单据
        '''
        self.handle.switch_users("单位资产管理员")
        self.handle.click_two_level_menu("出租 (借)")
        self.__switch_iframe()
        self.handle.click_element("通用", "勾选卡片", 0)
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
    def chuzu_ss(self):
        '''
        送审
        '''
        self.handle.switch_users("单位资产管理员")
        self.handle.click_two_level_menu("出租 (借)")
        self.__switch_iframe()
        self.handle.click_element("出租", "待送审")
        self.handle.click_element("通用", "勾选卡片", 0)
        self.handle.click_element("出租", "送审")
        time.sleep(1)
        self.handle.click_element("通用", "确定")

    #通过
    def chuzu_tg(self):
        '''
        通过
        '''
        self.handle.switch_users("单位资产管理员")
        self.handle.click_two_level_menu("出租 (借)")
        self.__switch_iframe()
        self.handle.click_element("出租", "审批中")
        time.sleep(1)
        self.handle.click_element("出租", "通过", 0)
        time.sleep(1)
        self.handle.click_element("通用", "确定")

    #执行
    def chuzu_zhix(self):
        '''
        执行
        '''
        self.handle.switch_users("单位资产管理员")
        self.handle.click_two_level_menu("出租 (借)")
        self.__switch_iframe()
        self.handle.click_element("出租", "已审批")
        self.handle.click_element("出租", "执行出租(借)")
        time.sleep(1)
        self.handle.click_element("通用", "确定")
        if self.__get_message() == "出租(借)成功":
            return True
        else:
            return False

    #登记收益
    def chuzu_shouyi(self, value):
        '''
        登记收益
        value:暂存  送财务部门
        '''
        self.handle.switch_users("单位资产管理员")
        self.handle.click_two_level_menu("出租 (借)")
        self.__switch_iframe()
        self.handle.click_element("出租", "出租(借)中")
        self.handle.click_element("出租", "登记收益", 0)
        time.sleep(1)
        self.handle.click_element("通用", "输入框", 0)
        self.handle.click_element("出租", "今天")
        self.handle.send_value("通用", "输入框", 1000, 1)
        self.handle.click_element("出租", value)

    #收回
    def chuzu_shouh(self):
        '''
        出租资产收回
        '''
        self.handle.switch_users("单位资产管理员")
        self.handle.click_two_level_menu("出租 (借)")
        self.__switch_iframe()
        self.handle.click_element("出租", "出租(借)中")
        self.handle.click_element("出租", "提前收回")
        time.sleep(1)
        self.handle.click_element("通用", "确定")
        if self.__get_message() == "收回成功":
            return True
        else:
            return False


if __name__ == "__main__":
    driver = webdriver.Chrome()
    a = ChuzPage(driver)
    driver.get('http://58.246.240.154:7878/zl/179107')
    driver.maximize_window()
    time.sleep(1)
    a.send_value('登录', "username", "ss")
    a.send_value('登录', "password", "123qwe")
    time.sleep(1)
    a.click_element('登录', 'login')
    time.sleep(2)
    print(a.chuzu_shouyi())
