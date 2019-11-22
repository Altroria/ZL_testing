#coding=utf-8
'''
验收管理页面
'''
import sys
import os
sys.path.append(os.path.join(os.getcwd()))
from selenium import webdriver
import time
from base.base_handle import BaseHandle


class YansglPage():
    def __init__(self, driver):
        #Base__init__(self, driver)
        self.handle = BaseHandle(driver)

    #切换至待验收iframe
    def switch_iframe(self):
        self.handle.switch_iframe("iframe", "iframe_yansgl")

    #填写通用卡片资料
    def __send_card_data(self, value):
        self.handle.send_value("验收管理", "卡片信息", value, 3)
        #self.handle.caledar("验收管理", "卡片信息", date, 8)
        self.handle.click_element("验收管理", "卡片信息", 8)
        self.handle.click_element("通用", "今天")
        self.handle.click_element("验收管理", "保存")

    #获取提示信息
    def __get_message(self):
        try:
            self.handle.wait_element('message', 'accept_message')
            message_text = self.handle.get_element('message',
                                                   'accept_message').text
        except:
            message_text = None
        return message_text

    #新增卡片
    @BaseHandle.functional_combination("单位资产管理员", "验收管理")
    def add_card(self, value, card_value):
        '''
        --->待验收<---
        新增卡片and增加同类型卡片
        '''
        self.handle.click_element("验收管理", "增加")
        if card_value != None:
            self.handle.click_element("验收管理", "新增资产")
            self.handle.switch_iframe()
            self.handle.switch_iframe("iframe", "iframe1")
            time.sleep(2)
            self.handle.choice_first_class(card_value)
            self.handle.click_element("验收管理", "确定")
            time.sleep(2)
            self.handle.switch_iframe()
            self.handle.switch_iframe("iframe", "iframe2")
        else:
            self.handle.click_element("验收管理", "新增同类型资产")
            self.handle.click_element("通用", "勾选卡片", 0)
            self.handle.click_element("验收管理", "确认添加")
            time.sleep(2)
            self.handle.switch_iframe()
            self.handle.switch_iframe("iframe", "iframe1")
        self.__send_card_data(value)

    #开始验收
    @BaseHandle.functional_combination("单位资产管理员", "验收管理", index=[1])
    def start_acceptance(self):
        '''
        开始验收
        '''
        self.handle.click_element("验收管理", "开始验收")
        time.sleep(1)

    #验收通过
    @BaseHandle.functional_combination("单位资产管理员", "验收管理", "验收中", index=[1])
    def yansgl_pass(self):
        '''
        验收通过
        '''
        time.sleep(0.5)
        self.handle.click_element("验收管理", "验收通过")
        time.sleep(0.5)
        self.handle.click_element("通用", "确定")
        time.sleep(1)

    #新增卡片成功
    def add_card_success(self, value, card_value):
        '''
        --->待验收<---
        新增卡片and增加同类型卡片
        '''
        old_lines = self.handle.get_database_lines("待验收")
        self.add_card(value, card_value)
        new_lines = self.handle.get_database_lines("待验收")
        if old_lines + 1 == new_lines:
            return True
        else:
            return False

    #开始验收成功
    def start_acceptance_success(self):
        old_lines = self.handle.get_database_lines("待验收")
        self.start_acceptance()
        new_lines = self.handle.get_database_lines("待验收")
        if old_lines - 1 == new_lines:
            return True
        else:
            return False

    #验收通过成功
    def yansgl_pass_success(self):
        '''
        验收通过
        '''
        self.yansgl_pass()
        if self.__get_message() == "验收已通过":
            return True
        else:
            return False


if __name__ == "__main__":
    driver = webdriver.Chrome()
    a = YansglPage(driver)
    driver.get('http://58.246.240.154:7878/zl/179333')
    a.handle.send_value('登录', "username", "ss")
    a.handle.send_value('登录', "password", "123")
    time.sleep(1)
    a.handle.click_element('登录', 'login')
    time.sleep(1)
    a.add_card("1000", "PC服务器")
