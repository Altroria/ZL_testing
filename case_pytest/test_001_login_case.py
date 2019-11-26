#coding=utf-8
'''
登陆
'''
import sys
import os
import pytest
import time
sys.path.append(os.path.join(os.getcwd()))
from base.browser_engine import BrowserEngine
from log.user_log import UserLog
#登陆界面
from page.login_page import LoginPage


class TestLoginCase():
    def setup_class(self):
        self.log = UserLog()
        self.logger = self.log.get_log()
        #初始化driver
        self.driver = BrowserEngine().init_driver()
        self.driver.get('http://58.246.240.154:7878/zl/179333')
        self.driver.maximize_window()
        self.login = LoginPage(self.driver)

    def teardown_class(self):
        self.log.close_handle()
        time.sleep(2)
        self.driver.close()

    def setup(self):
        self.logger.info("this is chrome")

    def teardown(self):
        self.driver.refresh()

    #用户名不存在
    def test_login_name_error(self):
        name_error = self.login.login_name_error("s", "123")
        assert name_error == True

    #用户名为空
    def test_login_name_none_error(self):
        name_none_error = self.login.login_name_none("1")
        assert name_none_error == True

    #密码错误
    def test_login_password_error(self):
        password_error = self.login.login_password_error("ss", "1")
        assert password_error == True

    #密码为空
    def test_login_password_none_error(self):
        password_none_error = self.login.login_password_none("ss")
        assert password_none_error == True

    #通过
    def test_login_success(self):
        success = self.login.login_success("ss", "123")
        assert success == True


if __name__ == "__main__":
    #pytest.main(["-s", "C:\\ZL_testing\\case_pytest\\test_01.py::TestLoginCase::test_login_name_error"]) # 执行指定用例
    pytest.main([
        "-s", "-v", "-q",
        "C:\\ZL_testing\\case_pytest\\test_001_login_case.py::TestLoginCase"
    ])
    pytest.main([
        "-s", "-v", "-q", "--lf",
        "C:\\ZL_testing\\case_pytest\\test_001_login_case.py::TestLoginCase::test_login_name_error"
    ])
