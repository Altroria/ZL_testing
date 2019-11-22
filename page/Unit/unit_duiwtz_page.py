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


class DuiwtzPage():
    def __init__(self, driver):
        #BaseHandle.__init__(self, driver)
        self.handle = BaseHandle(driver)

    #切换iframe
    def switch_iframe(self):
        self.handle.switch_iframe("iframe", "iframe_touz")

    #获取提示信息
    def __get_message(self):
        try:
            self.handle.wait_element('message', 'message_touzcg')
            message_text = self.handle.get_element('message',
                                                   'message_touzcg').text
        except:
            message_text = None
        return message_text

    #投资生成单据
    @BaseHandle.functional_combination("单位资产管理员", "对外投资", index=[1])
    def touz_scdj(self):
        self.handle.click_element("对外投资", "生成投资申请单")
        self.handle.click_element("通用", "输入框", 0)
        self.handle.click_element("对外投资", "初始投资")
        self.handle.click_element("通用", "确定")
        time.sleep(1)
        self.handle.click_element("对外投资", "下一步")
        time.sleep(1)
        self.handle.click_element("通用", "勾选卡片", 0)
        self.handle.click_element("对外投资", "下一步")
        time.sleep(1)
        self.handle.send_value("通用", "输入框", 1, 0)
        self.handle.send_value("通用", "输入框", 2, 3)
        self.handle.click_element("对外投资", "下一步")
        time.sleep(1)
        self.handle.click_element("对外投资", "编辑")
        self.handle.click_element("通用", "输入框", 2)
        self.handle.click_element("对外投资", "长期股权投资")
        self.handle.send_value("通用", "输入框", "哲凌科技", 3)
        self.handle.click_element("通用", "输入框", 4)
        self.handle.click_element("对外投资", "其他")
        self.handle.send_value("通用", "输入框", 2, 5)
        self.handle.send_value("通用", "输入框", 2, 6)
        #投资到期日
        data = self.handle.get_elements("通用", "输入框")[7].get_attribute('value')
        self.handle.caledar("通用", "输入框", data, 8)
        self.handle.click_element("通用", "输入框", 8)
        self.handle.send_value("通用", "输入框", 2, 9)
        self.handle.click_element("通用", "确定")
        self.handle.click_element("对外投资", "下一步")
        time.sleep(1)
        self.handle.send_value("通用", "输入框", 2, 0)
        self.handle.send_value("通用", "输入框", 2, 1)
        self.handle.send_value("通用", "输入框", 2, 2)
        self.handle.send_value("通用", "输入框", 2, 3)
        self.handle.send_value("通用", "输入框", 2, 4)
        self.handle.send_value("通用", "输入框", 2, 5)
        self.handle.click_element("对外投资", "附报材料")
        self.handle.click_element("对外投资", "附报材料_勾选", 0)
        self.handle.click_element("对外投资", "附报材料_勾选", 1)
        self.handle.click_element("对外投资", "附报材料_勾选", 3)
        self.handle.click_element("对外投资", "附报材料_勾选", 4)
        self.handle.click_element("对外投资", "附报材料_勾选", 5)
        self.handle.click_element("对外投资", "附报材料_勾选", 6)
        self.handle.click_element("对外投资", "附报材料_勾选", 7)
        self.handle.click_element("通用", "确定")

    #送审
    @BaseHandle.functional_combination("单位资产管理员", "对外投资", "待送审", index=[1])
    def touz_ss(self):
        self.handle.click_element("对外投资", "送审")
        time.sleep(1)
        self.handle.click_element("通用", "确定")

    #执行
    @BaseHandle.functional_combination("单位资产管理员", "对外投资", "待送审")
    def touz_zhix(self):
        self.handle.click_element("对外投资", "执行投资")
        self.handle.send_value("通用", "输入框", 100, 2)
        self.handle.click_element("通用", "确定")
        if self.__get_message() == "①登记对外投资信息":
            return True
        else:
            return False

    #执行成功
    def touz_zhix_success(self):
        self.touz_zhix()
        if self.__get_message() == "①登记对外投资信息":
            return True
        else:
            return False


if __name__ == "__main__":
    driver = webdriver.Chrome()
    a = DuiwtzPage(driver)
    driver.get('http://58.246.240.154:7878/zl/179333')
    driver.maximize_window()
    time.sleep(1)
    a.handle.send_value('登录', "username", "ss")
    a.handle.send_value('登录', "password", "123")
    time.sleep(1)
    a.handle.click_element('登录', 'login')
    time.sleep(2)
    print(a.touz_zhix_success())
