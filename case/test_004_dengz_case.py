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
        self.zl = make_date(self.driver)
        #前置：单位资产管理员新增未登账卡片
        self.zl.unit_suoyzc_wdengz()

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
        self.zl.unit_dengz.songcw()
        self.driver.refresh()
        success = self.zl.fin_dengz.dengz_success()
        self.assertTrue(success, "登账成功")

    #送财务登账-填发票号-财务退回
    def test_danw_dengz_tianfp_caiw_tui(self):
        self.driver.refresh()
        self.zl.unit_dengz.songcw(1000)
        self.driver.refresh()
        success = self.zl.fin_dengz.tuih_success()
        self.assertTrue(success, "退回成功")


if __name__ == "__main__":
    file_path = os.path.join(os.getcwd() + "/report/" + "test_case.html")
    f = open(file_path, 'wb')
    suite = unittest.TestSuite()
    suite.addTest(DengzCase('test_danw_dengz_butfp_caiw_dengz'))
    #suite.addTest(DengzCase('test_danw_dengz_tianfp_caiw_tui'))
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=f, title="全量测试报告", verbosity=2)
    runner.run(suite)
