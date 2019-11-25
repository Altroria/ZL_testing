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


class ShenlCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = UserLog()
        cls.logger = cls.log.get_log()
        cls.driver = BrowserEngine().init_driver()
        LoginPage(cls.driver).cookie_login()

    def setUp(self):
        self.driver.refresh()
        self.logger.info("配置管理")
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

    #使用人申领-部门退回
    def test_shiyr_sl_bum_th(self):
        self.zl.user_shenl.shenl_xinz("PC服务器")
        self.zl.user_shenl.shenl_tj()
        success = self.zl.dep_peiz.peiz_ss_success("退回")
        self.assertTrue(success, "使用人申领-部门退回")

    #使用人申领-部门同意
    def test_shiyr_sl_bum_ty(self):
        self.zl.user_shenl.shenl_xinz("PC服务器")
        self.zl.user_shenl.shenl_tj()
        success = self.zl.dep_peiz.peiz_ss_success("同意")
        self.assertTrue(success, "使用人申领-部门同意")

    #使用人申领-部门不同意
    def test_shiyr_sl_bum_bty(self):
        self.zl.user_shenl.shenl_xinz("PC服务器")
        self.zl.user_shenl.shenl_tj()
        success = self.zl.dep_peiz.peiz_ss_success("同意")
        self.assertTrue(success, "使用人申领-部门不同意")

    #使用人申领-部门送审-单位退回
    def test_shiyr_sl_bum_ss_danw_th(self):
        self.zl.user_shenl.shenl_xinz("PC服务器")
        self.zl.user_shenl.shenl_tj()
        self.zl.dep_peiz.peiz_ss("送审")
        self.driver.refresh()
        success = self.zl.unit_peiz.peiz_ss_success("退回")
        self.assertTrue(success, "使用人申领-部门送审-单位退回")

    #使用人申领-部门送审-单位同意
    def test_shiyr_sl_bum_ss_danw_ty(self):
        self.zl.user_shenl.shenl_xinz("PC服务器")
        self.zl.user_shenl.shenl_tj()
        self.zl.dep_peiz.peiz_ss("送审")
        self.driver.refresh()
        success = self.zl.unit_peiz.peiz_ss_success("同意")
        self.assertTrue(success, "使用人申领-部门送审-单位同意")

    #使用人申领-部门送审-单位不同意
    def test_shiyr_sl_bum_ss_danw_bty(self):
        self.zl.user_shenl.shenl_xinz("PC服务器")
        self.zl.user_shenl.shenl_tj()
        self.zl.dep_peiz.peiz_ss("送审")
        self.driver.refresh()
        success = self.zl.unit_peiz.peiz_ss_success("不同意")
        self.assertTrue(success, "使用人申领-部门送审-单位不同意")

    #部门申领-单位同意
    def test_bum_sl_danw_ty(self):
        self.zl.dep_peiz.peiz_tj("PC服务器")
        self.driver.refresh()
        self.zl.dep_peiz.peiz_ss("送审")
        self.driver.refresh()
        success = self.zl.unit_peiz.peiz_ss_success("同意")
        self.assertTrue(success, "部门申领-单位同意")


if __name__ == "__main__":
    file_path = os.path.join(os.getcwd() + "/report/" + "test_case.html")
    f = open(file_path, 'wb')
    suite = unittest.TestSuite()
    #suite.addTest(ShenlCase('test_shiyr_sl_bum_th'))
    #suite.addTest(ShenlCase('test_shiyr_sl_bum_ty'))
    #suite.addTest(ShenlCase('test_shiyr_sl_bum_ss_danw_th'))
    #suite.addTest(ShenlCase('test_shiyr_sl_bum_ss_danw_ty'))
    suite.addTest(ShenlCase('test_shiyr_sl_bum_ss_danw_bty'))
    suite.addTest(ShenlCase('test_bum_sl_danw_ty'))
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=f, title="全量测试报告", verbosity=2)
    runner.run(suite)
