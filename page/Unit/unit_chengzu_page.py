#coding=utf-8
'''
承租页面
'''

import sys
import os
sys.path.append(os.path.join(os.getcwd()))
from selenium import webdriver

import time
from base.base_handle import BaseHandle


class chengzu():
    def __init__(self, driver):
        self.handle = BaseHandle(driver)

    #切换iframe
    def switch_iframe(self):
        self.handle.switch_iframe("iframe", "iframe_chengzj")

    #获取提示
    def __get_message(self):
        try:
            self.handle.switch_iframe()
            self.handle.wait_element('message', 'ty_message')
            message_text = self.handle.get_element('message',
                                                   'ty_message').text
        except:
            message_text = None
        return message_text

    #查看合同编号
    def __get_hetbh(self):
        try:
            het_message = self.handle.get_elements(
                "通用", "输入框")[15].get_attribute('value')
        except:
            het_message = None
        return het_message

    #承租借 填写卡片资料
    def __chengzj_card(self, het_value=111):
        time.sleep(1)
        self.handle.click_element("承租", "日期", 0)  # 取得日期
        self.handle.click_element("通用", "今天")
        self.handle.send_value("通用", "输入框", het_value, 15)  # 合同编号
        self.handle.click_element("承租", "日期", 3)  # 合同签订日期
        self.handle.click_element("通用", "今天")
        self.handle.send_value("通用", "输入框", "asd", 17)  # 合同签订人
        self.handle.click_element("承租", "日期", 4)  # 租赁期限
        self.handle.click_element("通用", "今天")
        self.handle.send_value("通用", "输入框", "1000", 20)  # 押金
        self.handle.send_value("通用", "输入框", "100000", 21)  # 租金总额
        self.handle.send_value("通用", "输入框", "10000", 22)  # 每期租金
        self.handle.send_value("通用", "输入框", "10", 23)  # 缴纳期数

    def __xvzu_card(self):
        #续租合同填写
        self.handle.send_value("通用", "输入框", "1000")  # 合同编号
        self.handle.click_element("承租", "日期")  # 合同签订日期
        self.handle.click_element("通用", "今天")

    @BaseHandle.functional_combination("单位资产管理员", "承租 (借)", "待承租 (借)")
    def xinz(self):
        '''
        新增承租资产
        '''
        self.handle.click_element("承租", "增加承租(借)资产")
        self.handle.click_element("承租", "新增承租资产")
        self.handle.switch_iframe()
        self.handle.switch_iframe("iframe", "iframe1")
        self.handle.choice_first_class("pc服务器")
        self.handle.click_element("承租", "确定")
        time.sleep(2)
        self.handle.switch_iframe()
        self.handle.switch_iframe("iframe", "iframe2")
        self.__chengzj_card()
        self.handle.click_element("承租", "保存")

    @BaseHandle.functional_combination(
        "单位资产管理员", "承租 (借)", "待承租 (借)", index=[1])
    def jiaofu(self):
        '''
        交付完成
        '''
        self.handle.click_element("承租", "交付完成")
        time.sleep(1)
        self.handle.click_element("通用", "确定")
        time.sleep(1)
        self.handle.click_element("通用", "否")

    @BaseHandle.functional_combination("单位资产管理员", "承租 (借)", "承租 (借)中")
    def xvzu(self):
        '''
        续租
        '''
        self.handle.click_element("承租", "操作_申请续租")
        self.handle.switch_iframe("iframe", "iframe1")
        self.__xvzu_card()
        self.handle.switch_iframe()
        self.switch_iframe()
        self.handle.click_element("通用", "保存")
        time.sleep(1)
        self.handle.click_element("通用", "确定")

    @BaseHandle.functional_combination("单位资产管理员", "承租 (借)", "承租 (借)中")
    def tuih(self):
        '''
        退还
        '''
        self.handle.click_element("承租", "操作_退还")
        self.handle.click_element("通用", "确定")
        if self.__get_message() == "退还成功":
            return True
        else:
            return False

    @BaseHandle.functional_combination(
        "单位资产管理员", "承租 (借)", "承租 (借)中", index=[1, 2])
    def pilth(self):
        '''
        批量退还
        '''
        self.handle.click_element("承租", "批量退还")
        self.handle.click_element("通用", "确定")
        if self.__get_message() == "退还成功":
            return True
        else:
            return False

    @BaseHandle.functional_combination("单位资产管理员", "承租 (借)", "承租 (借)完成")
    def zaicxz(self):
        '''
        承借完成, 再次续租
        '''
        self.handle.click_element("承租", "操作_再次续租")
        self.handle.click_element("通用", "确定")
        time.sleep(1)
        self.handle.switch_iframe()
        self.handle.switch_iframe("iframe", "iframe1")
        self.__chengzj_card(het_value=222)
        self.handle.click_element("承租", "保存")
        time.sleep(1)

    def xvzu_success(self):
        '''
        续租成功
        '''
        self.xvzu()
        if self.__get_message() == "续租成功":
            return True
        else:
            return False

    def tuih_success(self):
        '''
        退还成功
        '''
        self.tuih()
        if self.__get_message() == "退还成功":
            return True
        else:
            return False

    def pilth_success(self):
        '''
        批量退还
        '''
        self.pilth()
        if self.__get_message() == "退还成功":
            return True
        else:
            return False

    def zaicxz_success(self):
        '''
        承借完成, 再次续租
        '''
        self.zaicxz()
        time.sleep(1)
        self.handle.switch_iframe()
        self.switch_iframe()
        self.handle.click_element("承租", "待承租 (借)")
        self.handle.switch_iframe()
        self.switch_iframe()
        self.handle.click_element("承租", "详细信息")
        self.handle.switch_iframe()
        self.handle.switch_iframe("iframe", "iframe2")
        if self.__get_hetbh() == "222":
            return True
        else:
            return False


if __name__ == "__main__":
    driver = webdriver.Chrome()
    a = chengzu(driver)
    driver.get('http://58.246.240.154:7878/zl/179333')
    driver.maximize_window()
    time.sleep(1)
    a.handle.send_value('登录', "username", "ss")
    a.handle.send_value('登录', "password", "123")
    time.sleep(1)
    a.handle.click_element('登录', 'login')
    time.sleep(2)
    print(1111111111111)
    print(a.zaicxz_success())
