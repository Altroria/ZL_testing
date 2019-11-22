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
    def switch_iframe(self):
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

    @BaseHandle.functional_combination("部门资产管理员", "配置管理")
    def peiz_tj(self, card_value="PC服务器"):
        '''
        增加申领
        card_value:资产分类，默认PC服务器
        '''
        self.handle.click_element("配置管理", "申领")
        self.handle.switch_iframe()
        self.handle.switch_iframe("iframe", "iframe1")
        time.sleep(2)
        self.handle.choice_first_class(card_value)
        self.handle.click_element("验收管理", "确定")
        time.sleep(2)
        self.handle.switch_iframe()
        self.switch_iframe()
        self.handle.click_element("通用", "输入框", 6)
        time.sleep(1)
        self.handle.click_element("配置管理", "办公使用")
        self.handle.click_element("通用", "确定")

    @BaseHandle.functional_combination("部门资产管理员", "配置管理", index=[1])
    def peiz_ss(self, value="同意"):
        '''
        部门审核
        value:退回、送审、同意、不同意
        '''
        self.handle.click_element("配置管理", "审核")
        self.handle.switch_iframe()
        self.handle.switch_iframe("iframe", "iframe1")
        self.handle.click_element("通用", value)
        self.handle.click_element("配置管理", "保存")

    def assert_peiz_ss_success(self, value="同意"):
        '''
        部门审核
        value:退回、送审、同意、不同意
        '''
        self.peiz_ss(value)
        if self.__get_message() == "审核成功！":
            return True
        else:
            return False


if __name__ == "__main__":
    driver = webdriver.Chrome()
    a = DepPeizlPage(driver)
    driver.get('http://58.246.240.154:7878/zl/179333')
    time.sleep(1)
    a.handle.send_value('登录', "username", "ss")
    a.handle.send_value('登录', "password", "123")
    driver.maximize_window()
    time.sleep(1)
    a.handle.click_element('登录', 'login')
    time.sleep(2)
    a.peiz_tj()
    print(a.peiz_ss())
