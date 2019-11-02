#coding=utf-8
'''
通用操作层
'''
import sys
import os
sys.path.append(os.path.join(os.getcwd()))
from selenium import webdriver

from base.base_class import SeleniumDriver
import time


class BaseHandle(SeleniumDriver):
    def __init__(self, driver):
        SeleniumDriver.__init__(self, driver)

    # 判断当前角色
    def get_role(self):
        self.wait_element('通用', 'role')
        role = self.get_element('通用', 'role').text
        return role

    # 点击一级菜单
    def click_first_class_menu(self, value):
        self.switch_iframe()
        self.click_element('菜单', value)

    #点击二级菜单
    def click_two_level_menu(self, value):
        self.switch_iframe()
        try:
            role_value = self.get_role()
            role_name = role_value.split('-')[0]
        except:
            role_name = "后台管理"
        menu_name, menu_value = self.get_menu_value(role_name, value)
        try:
            if value == '资产转移' and role_name == '部门资产管理员':
                self.click_element('二级菜单', '部门_资产转移')
            elif value == '资产转移' and role_name == '单位资产管理员':
                self.click_element('二级菜单', '单位_资产转移')
            else:
                self.click_element('二级菜单', menu_value)
        except:
            self.click_first_class_menu(menu_name)
            time.sleep(0.5)
            if value == '资产转移' and role_name == '部门资产管理员':
                self.click_element('二级菜单', '部门_资产转移')
            elif value == '资产转移' and role_name == '单位资产管理员':
                self.click_element('二级菜单', '单位_资产转移')
            else:
                self.click_element('二级菜单', menu_value)

    #选择分类明细
    def choice_first_class(self, value):
        self.click_element("资产分类", "明细资产分类")
        try:
            #四级分类
            third_class, second_class, first_class = self.get_class_value(
                "资产分类", value)
            if first_class != "土地、房屋及构筑物":
                self.click_element("一级分类", first_class)
            time.sleep(0.3)
            self.click_element("二级分类", second_class)
            time.sleep(0.3)
            self.click_element("三级分类", third_class)
            time.sleep(0.3)
            self.click_element("四级分类", value)
        except:
            #三级分类
            try:
                second_class, first_class = self.get_class_value("资产分类", value)
                if first_class != "土地、房屋及构筑物":
                    self.click_element("一级分类", first_class)
                time.sleep(0.3)
                self.click_element("二级分类", second_class)
                time.sleep(0.3)
                self.click_element("三级分类", value)
            except:
                #五级级分类
                try:
                    fourth_class, third_class, second_class, first_class = self.get_class_value(
                        "资产分类", value)
                    if first_class != "土地、房屋及构筑物":
                        self.click_element("一级分类", first_class)
                    time.sleep(0.3)
                    self.click_element("二级分类", second_class)
                    time.sleep(0.3)
                    self.click_element("三级分类", third_class)
                    time.sleep(0.3)
                    self.click_element("四级分类", fourth_class)
                    time.sleep(0.3)
                    self.click_element("五级分类", value)
                except:
                    print("分类输入错误。请选择最末级分类、或者加上上级分类")

    #切换用户
    def switch_users(self, value):
        self.switch_iframe()
        role_value = self.get_role()
        role_name = role_value.split('-')[0]
        if role_name != value:
            self.click_element('通用', 'role')
            time.sleep(0.5)
            if value == '使用人':
                self.click_element('通用', 'user')
            elif value == '部门资产管理员':
                self.click_element('通用', 'departmental_Manager')
            elif value == '部门领导':
                self.click_element('通用', 'departmental_leadership')
            elif value == '单位资产管理员':
                self.click_element('通用', 'unit_Manager')
            elif value == '单位领导':
                self.click_element('通用', 'unit_leadership')
            else:
                self.click_element('通用', 'finance')
        else:
            return None

    #定位卡片list_infolist
    def card_infolist(self, by, info, index=0):
        '''
        购置日期、资产编号 栏
        '''
        return self.get_level_element("通用", "data_info", by, info, index)

    #定位卡片list_imglist
    def card_imglist(self, by, info, index=0):
        '''
        其他
        '''
        return self.get_level_element("通用", "data_img", by, info, index)

    #切换iframe
    def switch_iframe1(self):
        self.switch_iframe()
        self.switch_iframe("iframe", "iframe1")

    def switch_iframe2(self):
        self.switch_iframe()
        self.switch_iframe("iframe", "iframe2")

    def search_assets(self, value):
        '''
        搜索资产
        '''
        self.send_value("通用", "资产搜索框", value)
        self.click_element("通用", "搜索")

    def select_current_page(self):
        '''
        点击选择当前页
        '''
        self.switch_iframe_daidz()
        self.click_element("通用", "选择当前页", 7)

    def check_card(self):
        '''
        勾选卡片
        '''
        self.click_element("通用", "勾选卡片", 0)

    def export(self):
        '''
        导出
        '''
        self.click_element("通用", "_导出")


if __name__ == "__main__":
    driver = webdriver.Chrome()
    a = BaseHandle(driver)
    driver.get('http://58.246.240.154:7878/zl/179111')
    time.sleep(2)
    a.send_value('登录', "username", "ss")
    a.send_value('登录', "password", "123")
    a.click_element('登录', 'login')
    time.sleep(2)
    a.click_two_level_menu("验收管理")
    a.switch_iframe("iframe", "iframe_yansgl")
    a.click_element("验收管理", "增加")
    a.click_element("验收管理", "新增资产")
    a.switch_iframe()
    a.switch_iframe("iframe", "iframe1")
    a.choice_first_class("栽植机械")