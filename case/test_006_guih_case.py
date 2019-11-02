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
#单位：资产分配
from page.Unit.unit_zicfp_page import ZicfpPage
#使用人：所有资产-待收货
from page.User.user_shouy_page import UserShouyPage
#部门：所有资产-待收货
from page.Departmental.dep_shouy_page import DepShouyPage
#单位：所有资产-待收货
from page.Unit.unit_shouy_page import ShouyPage
#使用人：资产归还
from page.User.user_guih_page import UserGuihPage
#部门：资产归还
from page.Departmental.dep_guih_page import DepGuihPage


class GuihCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = UserLog()
        cls.logger = cls.log.get_log()
        cls.driver = BrowserEngine().init_driver()
        LoginPage(cls.driver).cookie_login()

    def setUp(self):
        self.driver.refresh()
        self.logger.info("归还")
        self.unit_y = YansglPage(self.driver)
        self.unit_fp = ZicfpPage(self.driver)
        self.user_sh = UserShouyPage(self.driver)
        self.dep_sh = DepShouyPage(self.driver)
        self.unit_sh = ShouyPage(self.driver)
        self.user_gh = UserGuihPage(self.driver)
        self.dep_gh = DepGuihPage(self.driver)
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

    #使用人归还-部门收货
    def test_shiyr_guih_bum_shouh(self):
        self.unit_fp.fenp("使用人")
        self.user_sh.receipt()
        self.user_gh.guih_pass()
        success = self.dep_sh.receipt()
        self.assertTrue(success, "收货成功")

    #部门归还-单位收货
    def test_bum_guih_danw_shouh(self):
        self.unit_fp.fenp("部门")
        self.dep_sh.receipt()
        self.dep_gh.guih_pass()
        success = self.unit_sh.receipt()
        self.assertTrue(success, "收货成功")


if __name__ == "__main__":
    file_path = os.path.join(os.getcwd() + "/report/" + "test_case.html")
    f = open(file_path, 'wb')
    suite = unittest.TestSuite()
    suite.addTest(GuihCase('test_shiyr_guih_bum_shouh'))
    suite.addTest(GuihCase('test_bum_guih_danw_shouh'))
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=f, title="全量测试报告", verbosity=2)
    runner.run(suite)
