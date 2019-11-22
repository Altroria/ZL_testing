#coding=utf-8
'''
资产分配页面
'''

import sys
import os
sys.path.append(os.path.join(os.getcwd()))
from selenium import webdriver

import time
from base.base_handle import BaseHandle


class DepZicfpPage():
    def __init__(self, driver):
        #BaseHandle.__init__(self, driver)
        self.handle = BaseHandle(driver)

    #切换iframe
    def switch_iframe(self):
        self.handle.switch_iframe("iframe", "iframe_fenp")

    #获取提示信息
    def __get_message(self):
        try:
            self.handle.switch_iframe()
            self.handle.wait_element('message', 'ty_message')
            message_text = self.handle.get_element('message',
                                                   'ty_message').text
        except:
            message_text = None
        return message_text

    #删除接收方
    def del_per(self):
        self.handle.click_element("资产分配", "取消接收方")
        time.sleep(0.5)
        self.handle.click_element("通用", "确定")

    #添加接收方
    def add_per(self):
        self.handle.click_element("资产分配", "添加接收方")
        time.sleep(1)
        self.handle.click_element("资产分配", "勾选添加接收方")
        self.handle.click_element("通用", "确定")

    @BaseHandle.functional_combination("部门资产管理员", "资产分配", index=[1])
    def fenp(self, value):
        '''
        分配
        value:使用人、部门
        '''
        self.handle.click_element("资产分配", "添加接收方")
        time.sleep(1)
        if value == "使用人":
            self.handle.click_element("资产分配", "勾选添加接收方")
        self.handle.click_element("通用", "确定")
        time.sleep(1)
        self.handle.click_element("资产分配", "分配")
        time.sleep(0.5)
        self.handle.click_element("通用", "确定")

    #取消分配
    @BaseHandle.functional_combination("部门资产管理员", "资产分配", "分配中", index=[1])
    def quxfp(self):
        self.handle.click_element("资产分配", "取消分配")
        time.sleep(0.5)
        self.handle.click_element("通用", "确定")

    #取消分配成功
    def quxfp_success(self):
        self.quxfp()
        if self.handle.get_zicfp_message() == "操作成功":
            return True
        else:
            return False

    #无接收方取消接收方
    @BaseHandle.functional_combination("部门资产管理员", "资产分配", index=[1])
    def del_personnel_error(self):
        if self.handle.get_element("资产分配", "新增部门人员") == None:
            self.__del()
        self.__del()
        if self.handle.get_element('error', 'fenp_error').text == "请添加分配人方可操作":
            return True
        else:
            return False

    #无接收方分配
    @BaseHandle.functional_combination("部门资产管理员", "资产分配", index=[1])
    def distribution_error(self):
        if self.handle.get_element("资产分配", "新增部门人员") == None:
            self.__del()
        self.handle.click_element("资产分配", "分配")
        if self.handle.get_element(
                'error', 'fenp_error').text.endswith('请先添加接收人或接收部门') == True:
            return True
        else:
            return False

    #添加接收方成功
    @BaseHandle.functional_combination("部门资产管理员", "资产分配", index=[1])
    def add_personnel_success(self):
        self.add_per()
        if self.__get_message() == "添加成功":
            return True
        else:
            return False

    #取消接受方成功
    @BaseHandle.functional_combination("部门资产管理员", "资产分配", index=[1])
    def del_personnel_success(self):
        self.del_per()
        if self.__get_message() == "删除成功":
            return True
        else:
            return False


if __name__ == "__main__":
    driver = webdriver.Chrome()
    a = DepZicfpPage(driver)
    driver.get('http://58.246.240.154:7878/zl/179111')
    a.handle.send_value('登录', "username", "ss")
    a.handle.send_value('登录', "password", "123")
    time.sleep(1)
    a.handle.click_element('登录', 'login')
    time.sleep(5)
    a.fenp("使用人")
