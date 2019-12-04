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

    def functional_combination(usr_value=None,
                               menu_value=None,
                               sign_value=None,
                               index=None,
                               search_value=None):
        '''
        装饰器：功能组合
        usr_value 切换用户
        menu_value 菜单
        index勾选卡片 数组类型
        search_value 搜索编号
        '''

        def decorate(func):
            def wrapper(self, *args, **kwargs):
                if usr_value != None:
                    #调用切换用户
                    self.handle.switch_users(usr_value)
                if menu_value != None:
                    #调用切换菜单
                    self.handle.switch_meun(menu_value)
                    self.switch_iframe()
                if sign_value != None:
                    #调用切换页签
                    try:
                        self.handle.switch_page_sign(sign_value)
                        if sign_value == "所有资产":
                            self.handle.click_element("首页", "图片列表模式")
                    except:
                        print("页签切换失败")
                if search_value != None:
                    #调用搜索
                    try:
                        self.search_assets(search_value)
                    except:
                        print("搜索卡片失败")
                if index != None:
                    if index == "全选":
                        try:
                            self.handle.click_element("通用", "全选")
                        except:
                            print("全选错误")
                    elif index == "选择当前页":
                        try:
                            self.handle.click_element("通用", "选择当前页")
                        except:
                            print("选择当前页错误")
                    else:
                        #调用点击卡片
                        try:
                            time.sleep(3)
                            self.handle.check_card(index)
                        except:
                            print("勾选卡片错误")
                return func(self, *args, **kwargs)

            return wrapper  # 形成闭包

        return decorate

    # 判断当前角色
    def get_role(self):
        self.wait_element('角色', 'role')
        role = self.get_element('角色', 'role').text
        role_name = role.split('-')[0]
        return role_name

    # 点击一级菜单
    def click_first_class_menu(self, value):
        self.switch_iframe()
        self.click_element('菜单', value)

    #点击二级菜单
    def click_two_level_menu(self, value):
        self.switch_iframe()
        try:
            role_name = self.get_role()
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
        time.sleep(3)
        try:
            #四级分类
            third_class, second_class, first_class = self.get_class_value(
                "资产分类", value)
            if first_class != "土地、房屋及构筑物":
                self.click_element("一级分类", first_class)
            time.sleep(0.5)
            self.click_element("二级分类", second_class)
            time.sleep(0.5)
            self.click_element("三级分类", third_class)
            time.sleep(0.5)
            self.click_element("四级分类", value)
        except:
            #三级分类
            try:
                second_class, first_class = self.get_class_value("资产分类", value)
                if first_class != "土地、房屋及构筑物":
                    self.click_element("一级分类", first_class)
                time.sleep(0.5)
                self.click_element("二级分类", second_class)
                time.sleep(0.5)
                self.click_element("三级分类", value)
            except:
                #五级级分类
                try:
                    fourth_class, third_class, second_class, first_class = self.get_class_value(
                        "资产分类", value)
                    if first_class != "土地、房屋及构筑物":
                        self.click_element("一级分类", first_class)
                    time.sleep(0.5)
                    self.click_element("二级分类", second_class)
                    time.sleep(0.5)
                    self.click_element("三级分类", third_class)
                    time.sleep(0.5)
                    self.click_element("四级分类", fourth_class)
                    time.sleep(0.5)
                    self.click_element("五级分类", value)
                except:
                    print("分类输入错误。请选择最末级分类、或者加上上级分类")

    #切换用户
    def switch_users(self, value):
        self.switch_iframe()
        role_value = self.get_role()
        role_name = role_value.split('-')[0]
        if role_name != value:
            self.click_element('角色', 'role')
            time.sleep(0.5)
            if value == '使用人':
                self.click_element('角色', 'user')
            elif value == '部门资产管理员':
                self.click_element('角色', 'departmental_Manager')
            elif value == '部门领导':
                self.click_element('角色', 'departmental_leadership')
            elif value == '单位资产管理员':
                self.click_element('角色', 'unit_Manager')
            elif value == '单位领导':
                self.click_element('角色', 'unit_leadership')
            else:
                self.click_element('角色', 'finance')
        else:
            return None

    #切换菜单
    def switch_meun(self, value):
        #判断当前用户
        role_value = self.get_role()
        if role_value == "使用人":
            if value == "资产转移" or value == "资产归还":
                self.click_two_level_menu(value)
            else:
                self.click_first_class_menu(value)
        elif role_value == "部门资产管理员":
            if value == "首页" or value == "配置管理" or value == "验收资产" or value == "资产盘点" or value == "维修管理" or value == "资产处置":
                self.click_first_class_menu(value)
            else:
                self.click_two_level_menu(value)
        elif role_value == "单位资产管理员":
            if value == "首页" or value == "配置管理" or value == "维修管理" or value == "资产盘点" or value == "资产处置" or value == "收益管理":
                self.click_first_class_menu(value)
            else:
                self.click_two_level_menu(value)
        elif role_value == "财务制单人员":
            if value == "查询分析" or value == "汇总查询" or value == "历史查询" or value == "附属查询":
                self.click_two_level_menu(value)
            else:
                self.click_first_class_menu(value)

    #切换页签
    def switch_page_sign(self, value):
        self.click_element("页签", value)

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

    def search_assets(self, value):
        '''
        搜索资产
        '''
        self.send_value("通用", "资产搜索框", value)
        self.click_element("通用", "搜索")

    #勾选卡片
    def check_card(self, index):
        '''
        勾选卡片
        '''
        n = len(index)
        counter = 1
        while counter <= n:
            self.wait_element("通用", "勾选卡片")
            self.click_element("通用", "勾选卡片", index[counter - 1] - 1)
            counter += 1

    def export(self):
        '''
        导出
        '''
        self.click_element("通用", "_导出")

    #添加资产
    def add_assets(self, index):
        time.sleep(2)
        self.click_element("通用", "添加资产")
        self.switch_iframe("iframe", "iframe1")
        aa = self.get_elements("通用", "资产编号_02")[0].text
        self.check_card(index)
        self.click_element("通用", "确定_01")
        self.click_element("通用", "确定")
        return aa

if __name__ == "__main__":
    driver = webdriver.Chrome()
    a = BaseHandle(driver)
    driver.get('http://58.246.240.154:7878/zl/179333')
    time.sleep(2)
    a.send_value('登录', "username", "ss")
    a.send_value('登录', "password", "123")
    a.click_element('登录', 'login')
    time.sleep(2)
    a.switch_meun("资产收回")
    a.switch_iframe("iframe", "iframe_shouh")
    a.search_assets("123")
    '''
    a.switch_iframe("iframe", "iframe_yansgl")
    a.click_element("验收管理", "增加")
    a.click_element("验收管理", "新增资产")
    a.switch_iframe()
    a.switch_iframe("iframe", "iframe1")
    a.choice_first_class("栽植机械")
    '''
