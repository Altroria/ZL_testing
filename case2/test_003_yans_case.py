#coding=utf-8
import sys
import os
import unittest
import HTMLTestRunner
sys.path.append(os.path.join(os.getcwd()))
from base.browser_engine import BrowserEngine
from log.user_log import UserLog
from page.login_page import LoginPage
#验收管理界面
from page.Departmental.dep_yansgl_page import DepYansglPage
from page.Unit.unit_yansgl_page import YansglPage


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
        self.dep = DepYansglPage(self.driver)
        self.unit = YansglPage(self.driver)

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

    #部门新增资产
    def test_bum_add_new_card(self):
        self.dep.add_card(value="1000", date="2019-03-10", card_value="PC服务器")
        self.dep.start_acceptance()
        success = self.dep.yansgl_pass()
        self.assertTrue(success, "部门新增资产通过")

    #部门新增同类型资产
    def test_bum_add_card(self):
        self.dep.add_card(value="1000", date="2019-03-10")
        self.dep.start_acceptance()
        success = self.dep.yansgl_pass()
        self.assertTrue(success, "部门新增同类型资产通过")

    #单位新增资产
    def test_danw_add_new_card(self):
        self.unit.add_card(value="1000", date="2019-03-10", card_value="PC服务器")
        self.unit.start_acceptance()
        success = self.unit.yansgl_pass()
        self.assertTrue(success, "单位新增资产通过")

    #单位新增同类型资产
    def test_danw_add_card(self):
        self.unit.add_card(value="1000", date="2019-03-10")
        self.unit.start_acceptance()
        success = self.unit.yansgl_pass()
        self.assertTrue(success, "单位新增同类型资产通过")


if __name__ == "__main__":
    file_path = os.path.join(os.getcwd() + "/report/" + "test_case.html")
    f = open(file_path, 'wb')
    suite = unittest.TestSuite()
    suite.addTest(YansglCase('test_bum_add_new_card'))
    suite.addTest(YansglCase('test_bum_add_card'))
    suite.addTest(YansglCase('test_danw_add_new_card'))
    suite.addTest(YansglCase('test_danw_add_card'))
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=f, title="全量测试报告", verbosity=2)
    runner.run(suite)
