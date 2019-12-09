#coding=utf-8
'''
资产维修页面
'''

import sys
import os
sys.path.append(os.path.join(os.getcwd()))
from selenium import webdriver

import time
from base.base_handle import BaseHandle
from util.excel_util import ExcelUtil


class UserWeixPage():
    def __init__(self, driver):
        self.handle = BaseHandle(driver)

    #切换iframe
    def switch_iframe(self):
        self.handle.switch_iframe("iframe", "iframe_weixgl")

    #获取信息
    def get_message(self, value):
        try:
            self.handle.switch_iframe()
            self.handle.wait_element('message', value)
            message_text = self.handle.get_element('message', value).text
        except:
            message_text = None
        return message_text

    #勾选维修单审核
    @BaseHandle.functional_combination("使用人", "我要报修", "待提交", index=[1])
    def weix_ss(self, value):
        '''
        维修
        value:删除申请、提交申请
        '''
        self.handle.click_element("我要报修", value)
        self.handle.click_element("通用", "确定")
        time.sleep(3)

    #选择当前页维修单审核
    @BaseHandle.functional_combination("使用人", "我要报修", "待提交", index="选择当前页")
    def weix_dangq_ss(self, value):
        '''
        维修
        value:删除申请、提交申请
        '''
        self.handle.click_element("我要报修", value)
        self.handle.click_element("通用", "确定")
        time.sleep(3)

    #业务操作-提交申请
    #删除申请
    @BaseHandle.functional_combination("使用人", "我要报修", "待提交")
    def weix_yewcz(self, value):
        '''
        维修-业务操作
        value:操作_删除申请、操作_提交申请
        '''
        self.handle.click_element("我要报修", value, 0)
        self.handle.click_element("通用", "确定")
        time.sleep(3)

    #维修-添加资产
    @BaseHandle.functional_combination("使用人", "我要报修", "待提交")
    def add_weix_assets(self, index):
        aa = self.handle.add_assets(index)
        return aa

    # 修改维修方式
    @BaseHandle.functional_combination("使用人", "我要报修", "待提交")
    def change_mode(self, mode_value):
        '''
        修改维修方式
        mode_value: 维修方式
        '''
        self.handle.click_element('维修管理', "维修方式", 1)
        self.handle.click_element('维修管理', mode_value)

    # 填维修原因
    @BaseHandle.functional_combination("使用人", "我要报修", "待提交")
    def weix_reason(self, value):
        '''
        填维修原因
        value: 原因
        '''
        self.handle.click_element('维修管理', "输入维修原因")
        self.handle.send_value('维修管理', "维修原因", value)
        self.handle.click_element('维修管理', "维修方式", 1)

    # 待提交页面搜索功能

    #更多筛选

    #翻页

    #导出
    #@BaseHandle.functional_combination("使用人", "我要报修", "待提交", index=[1])
    def export_success(self):
        #self.handle.export()
        #获取导出文件信息
        ex = ExcelUtil("C:\\Users\\sunH\\Downloads\\待提交_20191206.xls")
        value = ex.get_data()
        return value


    #打印

    #删除维修单成功
    def weix_sahnc_success(self):
        self.weix_ss("删除申请")
        if self.get_message("删除成功") == "删除成功":
            return True
        else:
            return False

    #业务操作删除维修单成功
    def weix_yewcz_sahnc_success(self):
        self.weix_yewcz("操作_删除申请")
        if self.get_message("删除成功") == "删除成功":
            return True
        else:
            return False

    #选择当前页删除
    def weix_dangqy_sahnc_success(self):
        self.weix_dangq_ss("删除申请")
        if self.get_message("删除成功") == "删除成功":
            return True
        else:
            return False

    #维修-添加资产成功
    def add_assets_success(self):
        aa = self.add_weix_assets([1])
        self.handle.switch_iframe()
        self.switch_iframe()
        time.sleep(2)
        bb = self.handle.get_level_element("通用", "data_info", "通用", "资产编号",
                                           0).text
        if aa == bb[5:]:
            return True
        else:
            return False

    # 修改维修方式成功
    def change_mode_success(self, mode_value):
        self.change_mode(mode_value)
        if self.get_message("修改成功") == "修改成功":
            return True
        else:
            return False

    # 填维修原因
    def weix_reason_success(self, value):
        self.weix_reason(value)
        if self.get_message("修改成功") == "修改成功":
            return True
        else:
            return False

    #维修验收
    @BaseHandle.functional_combination("使用人", "我要报修", "已审核")
    def weix_yans(self, key):
        '''
        维修验收
        key:维修费用
        '''
        self.handle.click_element("维修管理", "维修验收")
        time.sleep(2)
        self.handle.click_element("维修管理", "选择维修商", 1)
        time.sleep(2)
        self.handle.click_element("维修管理", "勾选维修商")
        self.handle.click_element("维修管理", "选择维修商确定")
        self.handle.send_value("通用", "输入框", key, 2)
        self.handle.click_element("通用", "确定")


if __name__ == "__main__":
    driver = webdriver.Chrome()
    a = UserWeixPage(driver)
    driver.get('http://58.246.240.154:7878/zl/179333')
    time.sleep(1)
    a.handle.send_value('登录', "username", "ss")
    a.handle.send_value('登录', "password", "123")
    driver.maximize_window()
    time.sleep(1)
    a.handle.click_element('登录', 'login')
    time.sleep(5)
    print(a.export_success())
