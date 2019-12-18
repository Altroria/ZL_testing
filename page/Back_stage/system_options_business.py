#coding=utf-8
'''
系统配置选项业务层
'''

import sys
import os
sys.path.append(os.path.join(os.getcwd()))
from selenium import webdriver

import time
import json
#import pytesseract
import base64
import cx_Oracle
import pandas as pd
from ShowapiRequest import ShowapiRequest
from base.base_class import SeleniumDriver
from base.base_handle import BaseHandle

from tkinter import *
from PIL import Image


class SysBusiness(object):
    def __init__(self):
        self.myWindow = Tk()
        #设置标题
        self.myWindow.title('重建单位用户')

    # 连接oracle
    def Connect_oracle(self):
        self.address = 'zx/zl123456zl@164_XE'
        self.conn = cx_Oracle.connect(self.address)
        self.curs = self.conn.cursor()

    # 提交 断开Oracle
    def broken_oralce(self):
        self.curs.close()
        self.conn.commit()
        self.conn.close()

    def oracle_package(self):
        self.Connect_oracle()
        #声明变量
        #调用存储过程
        #删除单位
        try:
            P_ORGID = "7B2998E7A2CA4C32A5F9B58652EE7333"
            msg = self.curs.var(cx_Oracle.STRING)  # plsql出参
            args = [P_ORGID, msg]
            self.curs.callproc("AST_COMMON.CLEAR", args)  # 删除单位
        except cx_Oracle.Error as e:
            print(e)
        self.broken_oralce()

    def execute_sqlfile(self):
        self.Connect_oracle()
        try:
            ##读取SQL文件,获得sql语句的list
            with open(
                    'C:\ZL_testing\config\insert_bd_org.sql',
                    encoding='UTF-8') as f:
                sql_list = f.read().split(';')[:-1]  # sql文件最后一行加上;
                sql_list = [
                    x.replace('\n', ' ') if '\n' in x else x for x in sql_list
                ]  # 将每段sql里的换行符改成空格
            ##执行sql语句，使用循环执行sql语句
            for sql_item in sql_list:
                # print (sql_item)
                self.curs.execute(sql_item)
        except cx_Oracle.Error as e:
            print(e)
        finally:
            self.broken_oralce()

    def login(self):
        self.driver = webdriver.Chrome()
        self.sys_o = SeleniumDriver(self.driver)
        self.sys_h = BaseHandle(self.driver)
        self.driver.get('http://192.168.1.164:27979/zl/179333')
        self.sys_o.handle_windows("max")
        self.sys_o.send_value('登录', "username", "admin")
        self.sys_o.send_value('登录', "password", "zl123456zl")
        try:
            # 截取验证码
            self.driver.save_screenshot("C:/ZL_testing/image/ZL.png")
            code_element = self.sys_o.get_element('登录', "yanzm")
            left = code_element.location['x']
            top = code_element.location['y']
            right = code_element.size['width'] + left
            height = code_element.size['height'] + top
            im = Image.open('C:/ZL_testing/image/ZL.png')
            img = im.crop((left, top, right, height))
            img1 = img.resize((1024, 728))
            img1.save("C:/ZL_testing/image/yanzm.png")
            # 图片转base64
            f = open('C:/ZL_testing/image/yanzm.png', 'rb')  # 第一个参数图像路径
            ls_f = base64.b64encode(f.read())
            f.close()
            # Showapi识别验证码 精度高, 不免费
            r = ShowapiRequest("http://route.showapi.com/184-5", "126468",
                               "b76ac488b076469ea5f5a19d109e1bd3")
            r.addBodyPara("img_base64", ls_f)
            r.addBodyPara("typeId", "34")
            r.addBodyPara("convert_to_jpg", "0")
            r.addBodyPara("needMorePrecise", "0")
            res = r.post()
            yanzm_test = res.json()['showapi_res_body']['Result']
            '''
            # pytesseract识别验证码 精度低, 免费
            img1 = Image.open("C:/ZL_testing/image/yanzm.png")
            test = pytesseract.image_to_string(img1)
            '''
            self.sys_o.send_value('登录', "yanzm_key", yanzm_test)
        except:
            pass
        self.sys_o.click_element('登录', 'login')

    def switch_operation(self, value, date):
        self.sys_h.click_two_level_menu("系统选项配置")
        self.sys_o.switch_iframe("iframe", "iframe_Xitxxpzxg")
        self.sys_h.search_assets(value)
        time.sleep(1)
        element = self.sys_o.get_element("后台管理", "当前值_0")
        dangqz = element.get_attribute("value")
        if dangqz != date[0:1]:
            self.sys_o.click_element("后台管理", "下拉")
            time.sleep(1)
            self.sys_o.click_element("后台管理", date)
            time.sleep(1)
            self.sys_o.click_element("通用", "确定")

    def zhej(self):
        self.sys_h.click_two_level_menu("系统选项配置")
        self.sys_o.switch_iframe("iframe", "iframe_Xitxxpzxg")
        self.sys_h.search_assets("是否启用“新会计制度”")
        time.sleep(1)
        self.sys_o.click_element("后台管理", "设置")
        time.sleep(1)
        self.sys_o.click_element("后台管理", "启用")
        time.sleep(1)
        self.sys_o.click_element("后台管理", "折旧开关")
        time.sleep(1)
        self.sys_o.click_element("后台管理", "新会计制度基础版")
        time.sleep(1)
        self.sys_o.click_element("通用", "确定")
        time.sleep(2)

    def add_user(self):
        time.sleep(3)
        self.sys_o.switch_iframe("iframe", "iframe_adminHome")
        self.sys_o.click_element('后台管理', '核对部门人员信息')
        self.sys_o.right_click('后台管理', '单位树')
        self.sys_o.click_element('后台管理', '新增')
        self.sys_o.send_value('后台管理', '部门名称', '测试')
        self.sys_o.click_element('通用', '确定')
        time.sleep(2)
        self.sys_o.click_element('后台管理', '部门树')
        self.sys_o.click_element('后台管理', '新增部门人员')
        self.sys_o.send_value('通用', '输入框', 'ss', 0)
        self.sys_o.click_element('通用', '输入框', 3)
        self.sys_o.click_element('后台管理', '使用人')
        self.sys_o.click_element('后台管理', '部门资产管理员')
        self.sys_o.click_element('后台管理', '部门领导')
        self.sys_o.click_element('后台管理', '单位资产管理员')
        self.sys_o.click_element('后台管理', '单位领导')
        self.sys_o.click_element('后台管理', '财务制单人员')
        self.sys_o.click_element('通用', '输入框', 3)
        self.sys_o.click_element('后台管理', '职级', 2)
        self.sys_o.click_element('后台管理', '国家级正职')
        self.sys_o.click_element('通用', '确定')
        self.sys_o.switch_iframe()

    def init_user(self):
        time.sleep(3)
        self.sys_o.click_element('通用', '系统管理')
        time.sleep(1)
        self.sys_o.click_element('通用', '重新登录')
        self.sys_o.send_value('登录', "username", "ss")
        self.sys_o.send_value('登录', "password", "1")
        self.sys_o.click_element('登录', 'login')
        time.sleep(1)
        self.sys_o.send_value('通用', '输入框', '17621231905', 1)
        self.sys_o.send_value('通用', '输入框', '123', 3)
        self.sys_o.send_value('通用', '输入框', '123', 4)
        self.sys_o.click_element('后台管理', '保存')

    def close_driver(self):
        try:
            self.driver.close()
        except:
            pass
        self.myWindow.quit()

    def init_operation(self):
        self.switch_operation("是否启用“密码强度提示”", "否01")
        self.driver.refresh()
        self.switch_operation("是否启用“登录页面显示验证码”", "否01")
        self.driver.refresh()
        self.switch_operation("是否启用权限管理", "否01")
        self.driver.refresh()
        self.switch_operation("是否启用“送久其审批”", "否01")
        self.driver.refresh()
        self.zhej()

    def init_date(self):
        self.oracle_package()
        self.execute_sqlfile()
        self.login()
        self.init_operation()
        self.driver.refresh()
        self.add_user()
        self.init_user()

    def Button(self):
        Button(
            self.myWindow,
            text='初始化数据',
            font=('Helvetica 10 bold'),
            relief='raised',
            width=8,
            height=2,
            command=self.init_date).grid(
                row=0, column=0, sticky=W, padx=5, pady=5)
        Button(
            self.myWindow,
            text='退出',
            font=('Helvetica 10 bold'),
            relief='raised',
            command=self.close_driver,
            width=8,
            height=2).grid(
                row=0, column=1, sticky=W, padx=5, pady=5)
        self.myWindow.mainloop()


if __name__ == "__main__":
    a = SysBusiness()
    a.Button()
