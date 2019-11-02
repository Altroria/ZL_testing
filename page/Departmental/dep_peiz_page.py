#coding=utf-8
'''
部门配置管理
'''

import sys
import os
sys.path.append(os.path.join(os.getcwd()))
from selenium import webdriver

import time
from base.base_handle import BaseHandle


class DepPeizlPage():
    def __init__(self, driver):
        #BaseHandle.__init__(self, driver)
        self.handle = BaseHandle(driver)

    #切换iframe
    def __switch_iframe(self):
        self.handle.switch_iframe("iframe", "iframe_peizgl")

    #获取提示信息
    def __get_message(self):
        try:
            time.sleep(1)
            self.handle.switch_iframe()
            message_text = self.handle.get_element('message',
                                                   'ty_message').text
        except:
            message_text = None
        return message_text

    def peiz_tj(self, card_value="PC服务器"):
        '''
        增加申领
        card_value:资产分类，默认PC服务器
        '''
        self.handle.switch_users("部门资产管理员")
        self.handle.click_first_class_menu("配置管理")
        self.__switch_iframe()
        time.sleep(0.5)
        self.handle.click_element("配置管理", "申领")
        self.handle.switch_iframe()
        self.handle.switch_iframe("iframe", "iframe1")
        time.sleep(2)
        self.handle.choice_first_class(card_value)
        self.handle.click_element("验收管理", "确定")
        time.sleep(2)
        self.handle.switch_iframe()
        self.__switch_iframe()
        self.handle.click_element("通用", "输入框", 6)
        time.sleep(1)
        self.handle.click_element("配置管理", "办公使用")
        self.handle.click_element("通用", "确定")

    def peiz_ss(self, value):
        '''
        部门审核
        value:退回、送审、同意、不同意
        '''
        self.handle.switch_users("部门资产管理员")
        self.handle.click_first_class_menu("配置管理")
        self.__switch_iframe()
        time.sleep(0.5)
        self.handle.click_element("通用", "勾选卡片", 0)
        self.handle.click_element("配置管理", "审核")
        self.handle.switch_iframe()
        self.handle.switch_iframe("iframe", "iframe1")
        self.handle.click_element("通用", value)
        self.handle.click_element("配置管理", "保存")
        if self.__get_message() == "审核成功！":
            return True
        else:
            return False


if __name__ == "__main__":
    driver = webdriver.Chrome()
    a = DepPeizlPage(driver)
    driver.get('http://58.246.240.154:7878/zl/179107')
    time.sleep(1)
    a.send_value('登录', "username", "ss")
    a.send_value('登录', "password", "123qwe")
    driver.maximize_window()
    time.sleep(1)
    a.click_element('登录', 'login')
    time.sleep(2)
    print(a.peiz_ss("退回"))
