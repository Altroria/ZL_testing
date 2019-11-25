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


class YansglCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = UserLog()
        cls.logger = cls.log.get_log()
        cls.driver = BrowserEngine().init_driver()
        LoginPage(cls.driver).cookie_login()

    def setUp(self):
        self.driver.refresh()
        self.logger.info("验收")
        self.zl = make_date(self.driver)

    def tearDown(self):
        for method_name, error in self._outcome.errors:
            if error:
                case_name = self._testMethodName
                file_path = os.path.join(os.getcwd() + "/image/" + case_name + ".png")
                self.driver.save_screenshot(file_path)

    @classmethod
    def tearDownClass(cls):
        cls.log.close_handle()
        cls.driver.close()

    #部门新增资产
    def test_bum_add_new_card(self):
        self.zl.dep_yans.add_card(value="1000", card_value="PC服务器")
        self.zl.dep_yans.start_acceptance()
        success = self.zl.dep_yans.yansgl_pass_success()
        self.assertTrue(success, "部门新增资产通过")

    #部门新增同类型资产
    def test_bum_add_card(self):
        self.zl.dep_yans.add_card(value="1000")
        self.zl.dep_yans.start_acceptance()
        success = self.zl.dep_yans.yansgl_pass_success()
        self.assertTrue(success, "部门新增同类型资产通过")

    #单位新增资产
    def test_danw_add_new_card(self):
        self.zl.unit_yans.add_card(value="1000", card_value="PC服务器")
        self.zl.unit_yans.start_acceptance()
        self.driver.refresh()
        success = self.zl.unit_yans.yansgl_pass_success()
        self.assertTrue(success, "单位新增资产通过")

    #单位新增同类型资产
    def test_danw_add_card(self):
        self.zl.unit_yans.add_card(value="1000", card_value="PC服务器")
        self.zl.unit_yans.start_acceptance()
        self.driver.refresh()
        success = self.zl.unit_yans.yansgl_pass_success()
        self.assertTrue(success, "单位新增同类型资产通过")


if __name__ == "__main__":
    file_path = os.path.join(os.getcwd() + "/report/" + "test_case.html")
    f = open(file_path, 'wb')
    suite = unittest.TestSuite()
    #suite.addTest(YansglCase('test_bum_add_new_card'))
    #suite.addTest(YansglCase('test_bum_add_card'))
    suite.addTest(YansglCase('test_danw_add_new_card'))
    suite.addTest(YansglCase('test_danw_add_card'))
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=f, title="全量测试报告", verbosity=2)
    runner.run(suite)
