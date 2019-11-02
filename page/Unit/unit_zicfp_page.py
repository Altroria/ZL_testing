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


class ZicfpPage():
    def __init__(self, driver):
        #BaseHandle.__init__(self, driver)
        self.handle = BaseHandle(driver)

    #切换iframe
    def __switch_iframe(self):
        self.handle.switch_iframe("iframe", "iframe_fenp")

    #删除接收方
    def __del(self):
        self.handle.click_element("资产分配", "取消接收方")
        time.sleep(0.5)
        self.handle.click_element("通用", "确定")

    #添加接收方
    def __add(self):
        self.handle.click_element("资产分配", "添加接收方")
        time.sleep(1)
        self.handle.click_element("资产分配", "勾选添加接收方")
        self.handle.click_element("通用", "确定")

    #获取提示信息
    def __get_zicfp_pass_message(self):
        try:
            self.handle.switch_iframe()
            self.handle.wait_element('message', 'ty_message')
            message_text = self.handle.get_element('message',
                                                   'ty_message').text
        except:
            message_text = None
        return message_text

    #添加接收方
    def add_personnel(self):
        '''
        添加接收方
        '''
        self.handle.switch_users("单位资产管理员")
        self.handle.click_two_level_menu("资产分配")
        self.__switch_iframe()
        self.handle.click_element("通用", "勾选卡片", 0)
        self.__add()
        if self.__get_zicfp_pass_message() == "添加成功":
            return True
        else:
            return False

    #取消接受方
    def del_personnel(self):
        '''
        取消接受方
        '''
        self.handle.switch_users("单位资产管理员")
        self.handle.click_two_level_menu("资产分配")
        self.__switch_iframe()
        self.handle.click_element("通用", "勾选卡片", 0)
        if self.handle.get_element("资产分配", "新增部门人员") != None:
            self.handle.add_()
            time.sleep(1)
        self.__del()
        if self.handle.get_zicfp_pass_message() == "删除成功":
            return True
        else:
            return False

    #分配
    def fenp(self, value):
        '''
        分配
        value:使用人、部门
        '''
        self.handle.switch_users("单位资产管理员")
        self.handle.click_two_level_menu("资产分配")
        self.__switch_iframe()
        self.handle.click_element("通用", "勾选卡片", 0)
        self.handle.click_element("资产分配", "添加接收方")
        time.sleep(1)
        if value == "使用人":
            self.handle.click_element("资产分配", "勾选添加接收方")
        self.handle.click_element("通用", "确定")
        time.sleep(1)
        self.handle.click_element("资产分配", "分配")
        time.sleep(0.5)
        self.handle.click_element("通用", "确定")

    #无接收方取消接收方
    def del_personnel_error(self):
        '''
        无接收方取消接收方
        '''
        self.handle.switch_users("单位资产管理员")
        self.handle.click_two_level_menu("资产分配")
        self.__switch_iframe()
        self.handle.click_element("通用", "勾选卡片", 0)
        if self.handle.get_element("资产分配", "新增部门人员") == None:
            self.__del()
        self.__del()
        if self.handle.get_element('error', 'fenp_error').text == "请添加分配人方可操作":
            return True
        else:
            return False

    #无接收方分配
    def distribution_error(self):
        '''
        无接收方分配
        '''
        self.handle.switch_users("单位资产管理员")
        self.handle.click_two_level_menu("资产分配")
        self.__switch_iframe()
        self.handle.click_element("通用", "勾选卡片", 0)
        if self.handle.get_element("资产分配", "新增部门人员") == None:
            self.handle.del_()
        self.handle.click_element("资产分配", "分配")
        if self.handle.get_element(
                'error', 'fenp_error').text.endswith('请先添加接收人或接收部门') == True:
            return True
        else:
            return False

    #取消分配
    def quxfp(self):
        self.handle.switch_users("单位资产管理员")
        self.handle.click_two_level_menu("资产分配")
        self.__switch_iframe()
        self.handle.click_element("资产分配", "分配中")
        time.sleep(0.5)
        self.handle.click_element("通用", "勾选卡片", 0)
        self.handle.click_element("资产分配", "取消分配")
        time.sleep(0.5)
        self.handle.click_element("通用", "确定")
        if self.handle.get_zicfp_message() == "操作成功":
            return True
        else:
            return False

    def fp_daochu(self):
        '''
        分配导出
        '''
        self.handle.switch_users("单位资产管理员")
        self.handle.click_two_level_menu("资产分配")
        self.__switch_iframe()
        time.sleep(0.5)
        self.handle.click_element("通用", "勾选卡片", 0)
        self.handle.export()


if __name__ == "__main__":
    driver = webdriver.Chrome()
    a = ZicfpPage(driver)
    driver.get('http://58.246.240.154:7878/zl/179111')
    a.handle.send_value('登录', "username", "ss")
    a.handle.send_value('登录', "password", "123")
    time.sleep(1)
    a.handle.click_element('登录', 'login')
    time.sleep(5)
    a.fp_daochu()
