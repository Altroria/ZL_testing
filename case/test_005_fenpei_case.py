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


class FenpCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = UserLog()
        cls.logger = cls.log.get_log()
        cls.driver = BrowserEngine().init_driver()
        LoginPage(cls.driver).cookie_login()

    #前置
    def setUp(self):
        self.driver.refresh()
        self.logger.info("分配")
        self.zl = make_date(self.driver)
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

    #单位分配资产至部门
    def test_danw_fp_bum_shouh(self):
        self.zl.unit_fenp.fenp("部门")
        #检测点：部门收货
        success = self.zl.dep_shouy.receipt_success()
        self.assertTrue(success, "收货成功")

    #单位分配资产至使用人
    def test_danw_fp_shiyr_shouh(self):
        self.zl.unit_fenp.fenp("使用人")
        #检测点：使用人收货
        success = self.zl.user_shouy.receipt_success("确认收货")
        self.assertTrue(success, "收货成功")

    #部门分配资产
    def test_bum_fp_bum_shouh(self):
        self.zl.unit_fenp.fenp("部门")
        self.zl.dep_shouy.receipt("确认收货")
        self.zl.dep_fenp.fenp("使用人")
        #检测点：使用人收货
        success = self.zl.user_shouy.receipt_success()
        self.assertTrue(success, "收货成功")


if __name__ == "__main__":
    file_path = os.path.join(os.getcwd() + "/report/" + "test_case.html")
    f = open(file_path, 'wb')
    suite = unittest.TestSuite()
    suite.addTest(FenpCase('test_danw_fp_bum_shouh'))
    suite.addTest(FenpCase('test_danw_fp_shiyr_shouh'))
    suite.addTest(FenpCase('test_bum_fp_bum_shouh'))
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=f, title="全量测试报告", verbosity=2)
    runner.run(suite)
