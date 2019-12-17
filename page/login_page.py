#coding=utf-8
'''
登录业务层
'''
import sys
import os
sys.path.append(os.path.join(os.getcwd()))
from selenium import webdriver
import time
from config import settings
from base.base_handle import BaseHandle


class LoginPage(BaseHandle):
    def __init__(self, driver):
        BaseHandle.__init__(self, driver)

    def cookie_login(self):
        '''
        self.get_url(settings.zl)
        self.set_cookie()
        time.sleep(1)
        self.get_url(settings.danw)
        try:
            time.sleep(2)
            self.get_element('通用', 'users').text
        except:
            self.get_url(settings.zl)
            time.sleep(1)
            self.login_success(settings.name, settings.password)
            self.get_cookie()
        '''
        self.get_url(settings.zl)
        time.sleep(1)
        self.login_success(settings.name, settings.password)

    #输入用户名
    def send_user_name(self, username=None):
        self.send_value('登录', "username", username)

    #输入密码
    def send_user_password(self, password=None):
        self.send_value('登录', "password", password)

    #点击登录按钮
    def click_login(self):
        self.click_element('登录', 'login')

    #获取提示信息
    def get_prompt_message(self):
        try:
            time.sleep(1)
            message_text = self.get_element('error', 'login_error').text
        except:
            message_text = None
        return message_text

    #获取登陆名
    def get_personal_info(self):
        try:
            time.sleep(2)
            message_text = self.get_element('角色', 'users').text
        except:
            message_text = None
        return message_text

    #执行操作
    #数据驱动
    def login_function(self, username=None, password=None, asserText=None):
        self.send_user_name(username)
        self.send_user_password(password)
        self.click_login()
        if asserText == username and self.get_personal_info() == asserText:
            return True
        elif asserText != username and self.get_prompt_message() == asserText:
            return True
        else:
            return False

    #po模型
    def login(self, name=None, password=None):
        self.send_user_name(name)
        self.send_user_password(password)
        self.click_login()

    def login_name_none(self, password):
        self.send_user_password(password)
        self.click_login()
        if self.get_prompt_message() == "请输入用户名":
            return True
        else:
            return False

    def login_password_none(self, name):
        self.send_user_name(name)
        self.click_login()
        if self.get_prompt_message() == "请输入密码":
            return True
        else:
            return False

    def login_name_error(self, name, password):
        self.login(name, password)
        if self.get_prompt_message() == "用户不存在！":
            return True
        else:
            return False

    def login_password_error(self, name, password):
        self.login(name, password)
        if self.get_prompt_message() == "用户名或密码错误！":
            return True
        else:
            return False

    def login_success(self, name, password):
        self.login(name, password)
        if self.get_personal_info() == name:
            return True
        else:
            return False


if __name__ == "__main__":
    driver = webdriver.Chrome()
    a = LoginPage(driver)
    driver.get('http://58.246.240.154:7878/zl/179030')
    print(a.login_success("ss", "123"))
