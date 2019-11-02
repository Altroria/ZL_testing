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


class DepYansglPage():
    def __init__(self, driver):
        #BaseHandle.__init__(self, driver)
        self.handle = BaseHandle(driver)

    #切换至待验收iframe
    def __switch_iframe(self):
        self.handle.switch_iframe("iframe", "iframe_yansgl")

    #填写通用卡片资料
    def __send_card_data(self, value):
        self.handle.send_value("验收管理", "卡片信息", value, 3)
        #self.handle.caledar("验收管理", "卡片信息", date, 8)
        self.handle.click_element("验收管理", "卡片信息", 8)
        self.handle.click_element("通用", "今天")
        self.handle.click_element("验收管理", "保存")

    def __add_yansr(self):
        '''
        添加验收人
        '''
        self.handle.click_element("验收管理", "添加验收人")
        time.sleep(1)
        self.handle.click_element("验收管理", "勾选添加验收人")
        time.sleep(2)
        self.handle.click_element("通用", "确定")

    #获取提示信息
    def __get_message(self):
        try:
            self.handle.wait_element('message', 'accept_message')
            message_text = self.handle.get_element('message',
                                                   'accept_message').text
        except:
            message_text = None
        return message_text

    def add_card(self, value="1000", card_value=None):
        '''
        新增卡片and增加同类型卡片
        value:卡片价值
        card_value:卡片分类
        card_value=None时 增加同类型卡片
        '''
        self.handle.switch_users("部门资产管理员")
        old_lines = self.handle.get_database_lines("待验收")
        self.handle.click_first_class_menu("验收资产")
        self.__switch_iframe()
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
        new_lines = self.handle.get_database_lines("待验收")
        if old_lines + 1 == new_lines:
            return True
        else:
            return False

    def start_acceptance(self, value=None):
        '''
        开始验收
        value:添加验收人
        '''
        time.sleep(1)
        self.handle.switch_users("部门资产管理员")
        old_lines = self.handle.get_database_lines("待验收")
        self.handle.click_first_class_menu("验收资产")
        self.__switch_iframe()
        self.handle.click_element("通用", "勾选卡片", 0)
        time.sleep(1)
        if value == "添加验收人":
            self.__add_yansr()
        self.handle.click_element("验收管理", "开始验收")
        time.sleep(1)
        new_lines = self.handle.get_database_lines("待验收")
        if old_lines - 1 == new_lines:
            return True
        else:
            return False

    def yansgl_pass(self):
        '''
        验收通过
        '''
        self.handle.switch_users("部门资产管理员")
        self.handle.click_first_class_menu("验收资产")
        self.__switch_iframe()
        self.handle.click_element("验收管理", "验收中")
        self.handle.click_element("通用", "勾选卡片", 0)
        time.sleep(0.5)
        self.handle.click_element("验收管理", "验收通过")
        time.sleep(0.5)
        self.handle.click_element("通用", "确定")
        time.sleep(1)
        if self.__get_message() == "验收已通过":
            return True
        else:
            return False


if __name__ == "__main__":
    driver = webdriver.Chrome()
    a = DepYansglPage(driver)
    driver.get('http://58.246.240.154:7878/zl/179001')
    a.handle.send_value('登录', "username", "ss")
    a.handle.send_value('登录', "password", "123")
    time.sleep(1)
    a.handle.click_element('登录', 'login')
    time.sleep(1)
    a.start_acceptance("添加验收人")
