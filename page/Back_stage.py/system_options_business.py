#coding=utf-8
'''
系统配置选项业务层
'''

import sys
import os
sys.path.append(os.path.join(os.getcwd()))
from selenium import webdriver

import time
from base.base_class import SeleniumDriver
from base.base_handle import BaseHandle


class SysBusiness(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.sys_o = SeleniumDriver(self.driver)
        self.sys_h = BaseHandle(self.driver)

        self.driver.get('http://58.246.240.154:7878/zl/179201')
        self.sys_o.send_value('登录', "username", "admin")
        self.sys_o.send_value('登录', "password", "zl123456zl")
        self.sys_o.click_element('登录', 'login')
        self.sys_o.handle_windows("max")

    def switch_operation(self, value, date):
        self.sys_h.click_two_level_menu("系统选项配置")
        self.sys_o.switch_iframe("iframe", "iframe_Xitxxpzxg")
        self.sys_h.search_assets(value)
        time.sleep(1)
        try:
            element = self.sys_o.get_element("后台管理", "当前值_0")
            dangqz = element.get_attribute("value")
            if dangqz != date:
                self.sys_o.click_element("后台管理", "下拉")
                time.sleep(1)
                self.sys_o.click_element("后台管理", date)
                #self.driver.find_element_by_xpath('//*[@id="_easyui_combobox_i37_1"]')
                time.sleep(1)
                #self.sys_o.click_element("通用", "确定")
        except:
            element = self.sys_o.get_element("后台管理", "当前值_1")
            dangqz = element.text
            if dangqz != date:
                if date == '是':
                    date = '启用'
                else:
                    date = '不启用'
                self.sys_o.click_element("后台管理", "设置")
                time.sleep(0.5)
                self.sys_o.click_element("后台管理", date)
                time.sleep(0.5)
                self.sys_o.click_element("通用", "确定")


if __name__ == "__main__":
    a = SysBusiness()
    #a.switch_operation('是否启用“密码强度提示”', '是')
    a.switch_operation('是否启用“登录页面显示验证码”', '是')
    #a.switch_operation('是否启用“送久其审批”', '否')
