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
#部门：资产分配
from page.Departmental.dep_zicfp_page import DepZicfpPage
#单位：资产分配
from page.Unit.unit_zicfp_page import ZicfpPage
#使用人：所有资产-待收货
from page.User.user_shouy_page import UserShouyPage
#部门：所有资产-待收货
from page.Departmental.dep_shouy_page import DepShouyPage
#单位：所有资产-待收货
from page.Unit.unit_shouy_page import ShouyPage


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
        self.unit_y = YansglPage(self.driver)
        self.Dep_fp = DepZicfpPage(self.driver)
        self.unit_fp = ZicfpPage(self.driver)
        self.user_sh = UserShouyPage(self.driver)
        self.dep_sh = DepShouyPage(self.driver)
        self.unit_sh = ShouyPage(self.driver)
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

    #单位分配资产至部门
    def test_danw_fp_bum_shouh(self):
        self.unit_fp.fenp("部门")
        success = self.dep_sh.receipt()
        self.assertTrue(success, "收货成功")

    #单位分配资产至使用人
    def test_danw_fp_shiyr_shouh(self):
        self.unit_fp.fenp("使用人")
        success = self.user_sh.receipt()
        self.assertTrue(success, "收货成功")

    #部门分配资产
    def test_bum_fp_bum_shouh(self):
        self.Dep_fp.fenp("使用人")
        success = self.user_sh.receipt()
        self.assertTrue(success, "收货成功")


if __name__ == "__main__":
    file_path = os.path.join(os.getcwd() + "/report/" + "test_case.html")
    f = open(file_path, 'wb')
    suite = unittest.TestSuite()
    suite.addTest(FenpCase('test_danw_fp_bum_shouh'))
    #suite.addTest(FenpCase('test_danw_fp_shiyr_shouh'))
    #suite.addTest(FenpCase('test_bum_fp_bum_shouh'))
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=f, title="全量测试报告", verbosity=2)
    runner.run(suite)
