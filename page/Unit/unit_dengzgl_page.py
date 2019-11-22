#coding=utf-8
'''
登账管理页面
'''
import sys
import os
sys.path.append(os.path.join(os.getcwd()))
from selenium import webdriver

import time
from base.base_handle import BaseHandle


class DengzglPage():
    def __init__(self, driver):
        self.handle = BaseHandle(driver)

    #切换iframe
    def switch_iframe(self):
        self.handle.switch_iframe("iframe", "iframe_dengzgl")

    #获取提示信息
    def __get_message(self):
        try:
            self.handle.switch_iframe()
            time.sleep(0.75)
            message_text = self.handle.get_element("message", "message").text
        except:
            message_text = None
        return message_text

    @BaseHandle.functional_combination("单位资产管理员", "登账管理", "待登账", index=[1])
    def songcw(self, value=None):
        '''
        送财务部门
        value:发票号
        '''
        self.handle.click_element("登账管理", "送财务部门")
        if value != None:
            self.handle.send_value("登账管理", "发票号", value)
            time.sleep(1)
            self.handle.click_element("通用", "确定")
        else:
            self.handle.click_element("通用", "确定")
            time.sleep(1)
            self.handle.click_element("通用", "确定")

    #删除
    @BaseHandle.functional_combination("单位资产管理员", "登账管理", "待登账", index=[1])
    def del_card(self):
        self.handle.click_element("登账管理", "删除")
        time.sleep(1)
        self.handle.click_element("通用", "确定")
        time.sleep(1)

    #取消登账
    @BaseHandle.functional_combination("单位资产管理员", "登账管理", "登账中", index=[1])
    def cancel_entry(self):
        self.handle.click_element("登账管理", "取消登账")
        time.sleep(1)
        self.handle.click_element("通用", "确定")
        if self.__get_message() == "取消成功":
            return True
        else:
            return False

    #删除成功
    def del_card_success(self):
        old_lines = self.handle.get_database_lines("待登账")
        self.del_card()
        new_lines = self.handle.get_database_lines("待登账")
        if old_lines - 1 == new_lines:
            return True
        else:
            return False


if __name__ == "__main__":
    driver = webdriver.Chrome()
    a = DengzglPage(driver)
    driver.get('http://58.246.240.154:7878/zl/6666')
    a.send_value('登录', "username", "ss")
    a.send_value('登录', "password", "123")
    time.sleep(1)
    a.click_element('登录', 'login')
    time.sleep(2)
    print(a.songcw(1000))
