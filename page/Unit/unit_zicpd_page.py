#coding=utf-8
'''
资产盘点页面
'''
import time
import datetime
import sys
import os
sys.path.append(os.path.join(os.getcwd()))

from selenium import webdriver
from base.base_handle import BaseHandle


class ZicpdBusiness():
    def __init__(self, driver):
        self.handle = BaseHandle(driver)

    #切换iframe
    def __switch_iframe(self):
        self.handle.switch_iframe("iframe", "iframe_pand")

    #新增任务----------->新盘点
    def add_task(self):
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yesterday = today - oneday
        tomorrow = today + oneday
        self.handle.switch_users("单位资产管理员")
        self.handle.click_first_class_menu("资产盘点")
        self.__switch_iframe()
        self.handle.click_element("资产盘点", "新增")
        self.handle.send_value("资产盘点", "任务信息", "test1", 0)
        self.handle.caledar("资产盘点", "任务信息", str(yesterday), 2)
        self.handle.click_element("资产盘点", "任务信息", 2)
        self.handle.caledar("资产盘点", "任务信息", str(today), 3)
        self.handle.click_element("资产盘点", "任务信息", 3)
        self.handle.caledar("资产盘点", "任务信息", str(tomorrow), 4)
        self.handle.click_element("资产盘点", "任务信息", 4)
        self.handle.click_element("通用", "保存")
        time.sleep(0.5)
        self.handle.click_element("资产盘点", "发起", 0)
        time.sleep(0.5)
        self.handle.click_element("通用", "确定")
        time.sleep(0.5)
        if self.handle.get_element("资产盘点", "状态")[0].text == "已发起":
            return True
        else:
            return False

    #设置盘点信息----------->老盘点
    def set_date(self):
        self.handle.switch_users("单位资产管理员")
        self.handle.click_first_class_menu("资产盘点")
        self.switch_iframe_zicpd()
        self.handle.click_element("资产盘点", "设置盘点信息")
        time.sleep(0.5)
        self.handle.click_element("通用", "确定")

    def dish_one(self):
        self.handle.switch_users("单位资产管理员")
        self.handle.click_first_class_menu("资产盘点")
        self.switch_iframe_zicpd()
        self.handle.click_element("资产盘点", "未盘资产")
        self.handle.check_card()
        self.handle.click_element("资产盘点", "盘一下")
        self.handle.click_element("通用", "确定")

    def del_date(self):
        self.handle.switch_users("单位资产管理员")
        self.handle.click_first_class_menu("资产盘点")
        self.switch_iframe_zicpd()
        self.handle.click_element("资产盘点", "设置盘点信息")
        time.sleep(0.5)
        while self.handle.get_element("资产盘点", "删除") is not None:
            time.sleep(0.5)
            self.handle.click_element("资产盘点", "删除", 0)
            time.sleep(0.5)
            self.handle.click_element("资产盘点", "确定")
            time.sleep(0.5)
            self.handle.click_element("通用", "是")
            time.sleep(0.5)


if __name__ == "__main__":
    driver = webdriver.Chrome()
    a = ZicpdBusiness(driver)
    driver.get('http://58.246.240.154:7878/zl/179001')
    a.send_value('登录', "username", "ss")
    a.send_value('登录', "password", "123")
    time.sleep(1)
    a.click_element('登录', 'login')
    time.sleep(1)
    print(a.take_back())
