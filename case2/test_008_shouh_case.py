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
#部门：所有资产-待收货
from page.Departmental.dep_shouy_page import DepShouyPage
#单位：所有资产-待收货
from page.Unit.unit_shouy_page import ShouyPage
#部门：资产收回
from page.Departmental.dep_zicsh_page import DepZicshPage
#单位：资产收回
from page.Unit.unit_zicsh_page import ZicshPage


class ShouhCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = UserLog()
        cls.logger = cls.log.get_log()
        cls.driver = BrowserEngine().init_driver()
        LoginPage(cls.driver).cookie_login()

    def setUp(self):
        self.driver.refresh()
        self.logger.info("收回")
        self.unit_y = YansglPage(self.driver)
        self.dep_fp = DepZicfpPage(self.driver)
        self.unit_fp = ZicfpPage(self.driver)
        self.dep_sh = DepShouyPage(self.driver)
        self.unit_sh = ShouyPage(self.driver)
        self.dep_zcsh = DepZicshPage(self.driver)
        self.unit_zcsh = ZicshPage(self.driver)
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

    #部门收回卡片
    def test_bum_shouh(self):
        self.unit_fp.fenp("部门")
        self.unit_sh.receipt("确认收货")
        self.dep_fp.fenp("使用人")
        self.dep_sh.receipt()
        self.driver.refresh()
        success = self.dep_zcsh.take_back()
        self.assertTrue(success, "收回成功")

    #部门全部收回卡片
    @unittest.skip("全部收回功能已删除")
    def test_bum_shouh_all(self):
        self.unit_fp.fenp("部门")
        self.unit_sh.receipt("确认收货")
        self.dep_fp.fenp("使用人")
        self.dep_sh.receipt()
        self.driver.refresh()
        success = self.dep_zcsh.all_take_back()
        self.assertTrue(success, "收回成功")

    #单位收回卡片
    def test_danw_shouh(self):
        self.unit_fp.fenp("使用人")
        self.unit_sh.receipt("确认收货")
        self.driver.refresh()
        success = self.unit_zcsh.take_back()
        self.assertTrue(success, "收回成功")

    #单位全部收回卡片
    @unittest.skip("全部收回功能已删除")
    def test_danw_shouh_all(self):
        self.unit_fp.fenp("使用人")
        self.unit_sh.receipt("确认收货")
        self.driver.refresh()
        success = self.unit_zcsh.all_take_back()
        self.assertTrue(success, "收回成功")


if __name__ == "__main__":
    file_path = os.path.join(os.getcwd() + "/report/" + "test_case.html")
    f = open(file_path, 'wb')
    suite = unittest.TestSuite()
    suite.addTest(ShouhCase('test_bum_shouh'))
    suite.addTest(ShouhCase('test_bum_shouh_all'))
    suite.addTest(ShouhCase('test_danw_shouh'))
    suite.addTest(ShouhCase('test_danw_shouh_all'))
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=f, title="全量测试报告", verbosity=2)
    runner.run(suite)
