#coding=utf-8
'''
申领、配置
'''
import sys
import os
import unittest
import HTMLTestRunner
sys.path.append(os.path.join(os.getcwd()))
from base.browser_engine import BrowserEngine
from log.user_log import UserLog
from page.login_page import LoginPage
#申领、配置
from page.User.user_shenl_page import UserShenllPage
from page.Departmental.dep_peiz_page import DepPeizlPage
from page.Unit.unit_peiz_page import PeizlPage


class ShenlCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = UserLog()
        cls.logger = cls.log.get_log()
        #初始化driver
        cls.driver = BrowserEngine().init_driver()
        #cookie登陆
        LoginPage(cls.driver).cookie_login()

    def setUp(self):
        self.driver.refresh()
        self.logger.info("配置管理")
        self.user = UserShenllPage(self.driver)
        self.dep = DepPeizlPage(self.driver)
        self.unit = PeizlPage(self.driver)

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

    #使用人申领-部门退回
    def test_shiyr_sl_bum_th(self):
        self.user.shenl_tj("PC服务器")
        success = self.dep.peiz_ss("退回")
        self.assertTrue(success, "使用人申领-部门退回")

    #使用人申领-部门同意
    def test_shiyr_sl_bum_ty(self):
        self.user.shenl_tj("PC服务器")
        success = self.dep.peiz_ss("同意")
        self.assertTrue(success, "使用人申领-部门同意")

    #使用人申领-部门不同意
    def test_shiyr_sl_bum_bty(self):
        self.user.shenl_tj("PC服务器")
        success = self.dep.peiz_ss("同意")
        self.assertTrue(success, "使用人申领-部门不同意")

    #使用人申领-部门送审-单位退回
    def test_shiyr_sl_bum_ss_danw_th(self):
        self.user.shenl_tj("PC服务器")
        self.dep.peiz_ss("送审")
        success = self.unit.peiz_ss("退回")
        self.assertTrue(success, "使用人申领-部门送审-单位退回")

    #使用人申领-部门送审-单位同意
    def test_shiyr_sl_bum_ss_danw_ty(self):
        self.user.shenl_tj("PC服务器")
        self.dep.peiz_ss("送审")
        success = self.unit.peiz_ss("同意")
        self.assertTrue(success, "使用人申领-部门送审-单位同意")

    #使用人申领-部门送审-单位不同意
    def test_shiyr_sl_bum_ss_danw_bty(self):
        self.user.shenl_tj("PC服务器")
        self.dep.peiz_ss("送审")
        success = self.unit.peiz_ss("不同意")
        self.assertTrue(success, "使用人申领-部门送审-单位不同意")

    #部门申领-单位同意
    def test_bum_sl_danw_ty(self):
        self.dep.peiz_tj("PC服务器")
        self.driver.refresh()
        self.dep.peiz_ss("送审")
        success = self.unit.peiz_ss("同意")
        self.assertTrue(success, "部门申领-单位同意")


if __name__ == "__main__":
    file_path = os.path.join(os.getcwd() + "/report/" + "test_case.html")
    f = open(file_path, 'wb')
    suite = unittest.TestSuite()
    suite.addTest(ShenlCase('test_shiyr_sl_bum_th'))
    suite.addTest(ShenlCase('test_shiyr_sl_bum_ty'))
    suite.addTest(ShenlCase('test_shiyr_sl_bum_ss_danw_th'))
    suite.addTest(ShenlCase('test_shiyr_sl_bum_ss_danw_ty'))
    suite.addTest(ShenlCase('test_shiyr_sl_bum_ss_danw_bty'))
    suite.addTest(ShenlCase('test_bum_sl_danw_ty'))
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=f, title="全量测试报告", verbosity=2)
    runner.run(suite)
