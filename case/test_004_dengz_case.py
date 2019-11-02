#coding=utf-8
import sys
import os
import unittest
import HTMLTestRunner
sys.path.append(os.path.join(os.getcwd()))
from base.browser_engine import BrowserEngine
from log.user_log import UserLog
from page.login_page import LoginPage
#单位：验收管理
from page.Unit.unit_yansgl_page import YansglPage
#单位：登账管理
from page.Unit.unit_dengzgl_page import DengzglPage
#财务：新增资产
from page.Financial.fin_xinzzc_page import XinzzcPage


class DengzCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = UserLog()
        cls.logger = cls.log.get_log()
        cls.driver = BrowserEngine().init_driver()
        LoginPage(cls.driver).cookie_login()

    def setUp(self):
        self.driver.refresh()
        self.logger.info("登账")
        self.unit_y = YansglPage(self.driver)
        self.unit_d = DengzglPage(self.driver)
        self.fin = XinzzcPage(self.driver)
        #前置：单位资产管理员新增验收卡片、点击验收通过
        self.unit_y.add_card()
        self.unit_y.start_acceptance()
        self.unit_y.yansgl_pass()

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

    #送财务登账-不填发票号-财务登账
    def test_danw_dengz_butfp_caiw_dengz(self):
        self.driver.refresh()
        self.unit_d.songcw()
        self.driver.refresh()
        success = self.fin.dengz()
        self.assertTrue(success, "登账成功")

    #送财务登账-填发票号-财务退回
    def test_danw_dengz_tianfp_caiw_tui(self):
        self.driver.refresh()
        self.unit_d.songcw(1000)
        self.driver.refresh()
        success = self.fin.tuih()
        self.assertTrue(success, "退回成功")


if __name__ == "__main__":
    file_path = os.path.join(os.getcwd() + "/report/" + "test_case.html")
    f = open(file_path, 'wb')
    suite = unittest.TestSuite()
    suite.addTest(DengzCase('test_danw_dengz_butfp_caiw_dengz'))
    suite.addTest(DengzCase('test_danw_dengz_tianfp_caiw_tui'))
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=f, title="全量测试报告", verbosity=2)
    runner.run(suite)
