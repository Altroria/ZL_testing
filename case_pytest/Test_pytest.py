#coding=utf-8
'''
登陆
'''
import sys
import os
import unittest
import HTMLTestRunner
sys.path.append(os.path.join(os.getcwd()))
from base.browser_engine import BrowserEngine
from log.user_log import UserLog
import pytest
#登陆界面
from page.login_page import LoginPage


class LoginCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = UserLog()
        cls.logger = cls.log.get_log()
        #初始化driver
        cls.driver = BrowserEngine().init_driver()
        cls.driver.get('http://58.246.240.154:7878/zl/179001')
        cls.driver.maximize_window()

    def setUp(self):
        self.driver.refresh()
        self.logger.info("this is chrome")
        self.login = LoginPage(self.driver)

    def tearDown(self):
        for method_name, error in self._outcome.errors:
            if error:
                case_name = self._testMethodName
                file_path = os.path.join(os.getcwd() + "/image/" + case_name +
                                         ".png")
                self.driver.save_screenshot(file_path)

    @classmethod
    def tearDownClass(cls):
        cls.log.close_handle()
        cls.driver.close()

    #用户名不存在
    def test_login_name_error(self):
        name_error = self.login.login_name_error("s", "123")
        self.assertTrue(name_error, "case通过")

    #用户名为空
    def test_login_name_none_error(self):
        name_none_error = self.login.login_name_none("1")
        self.assertTrue(name_none_error, "case通过")

    #密码错误
    def test_login_password_error(self):
        password_error = self.login.login_password_error("ss", "1")
        self.assertTrue(password_error, "case通过")

    #密码为空
    def test_login_password_none_error(self):
        password_none_error = self.login.login_password_none("ss")
        self.assertTrue(password_none_error, "case通过")

    #通过
    #@unittest.skip("不执行第五条")
    def test_login_success(self):
        success = self.login.login_success("ss", "123")
        self.assertTrue(success, "case通过")


if __name__ == "__main__":
    '''
    #unittest.main()
    file_path = os.path.join(os.getcwd() + "/report/" + "first_case.html")
    f = open(file_path, 'wb')
    #suite容器
    suite = unittest.TestSuite()
    suite.addTest(LoginCase('test_login_name_error'))
    suite.addTest(LoginCase('test_login_name_none_error'))
    suite.addTest(LoginCase('test_login_password_error'))
    suite.addTest(LoginCase('test_login_password_none_error'))
    suite.addTest(LoginCase('test_login_success'))
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=f, title="全量测试报告", verbosity=2)
    runner.run(suite)
    '''
