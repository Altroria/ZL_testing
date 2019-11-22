#coding=utf-8
import sys
import os
import unittest
import HTMLTestRunner
sys.path.append(os.path.join(os.getcwd()))
#初始driver
from base.browser_engine import BrowserEngine
#日志
from log.user_log import UserLog
#登陆
from page.login_page import LoginPage
#数据初始 + 检测点模块
from page.date.make_date import make_date


class chengzu(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = UserLog()
        cls.logger = cls.log.get_log()
        cls.driver = BrowserEngine().init_driver()
        LoginPage(cls.driver).cookie_login()

    def setUp(self):
        self.driver.refresh()
        self.logger.info("出租")
        self.zl = make_date(self.driver)

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

    #承租——续租
    def test_chenz_xvzu_01(self):
        self.zl.unit_chengzu.xinz()
        self.zl.unit_chengzu.jiaofu()
        success = self.zl.unit_chengzu.xvzu()
        self.assertTrue(success, "续租成功")

    #承租——退还
    def test_chenz_tuihuan_01(self):
        self.zl.unit_chengzu.xinz()
        self.zl.unit_chengzu.jiaofu()
        success = self.zl.unit_chengzu.tuih()
        self.assertTrue(success, "退还成功")
        #承租完成的再次续租
        self.zl.handle.refresh_f5()
        success = self.zl.unit_chengzu.zaicxz()
        self.assertTrue(success, "续租成功")

    #承租——批量退还
    def test_chenz_tuihuan_02(self):
        self.zl.unit_chengzu.xinz()
        self.zl.unit_chengzu.jiaofu()
        success = self.zl.unit_chengzu.pilth()
        self.assertTrue(success, "退还成功")


if __name__ == "__main__":
    file_path = os.path.join(os.getcwd() + "/report/" + "test_case.html")
    f = open(file_path, 'wb')
    suite = unittest.TestSuite()
    #suite.addTest(chengzu('test_chenz_xvzu_01'))
    #suite.addTest(chengzu('test_chenz_tuihuan_01'))
    suite.addTest(chengzu('test_chenz_tuihuan_02'))
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=f, title="全量测试报告", verbosity=2)
    runner.run(suite)
