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
#使用人：资产转移
from page.User.user_zhuany_page import UserZhuanyPage
#部门：资产转移
from page.Departmental.dep_ziczy_page import DepZiczyPage
#单位：资产转移
from page.Unit.unit_ziczy_page import ZiczyPage


class ZhuanyCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = UserLog()
        cls.logger = cls.log.get_log()
        cls.driver = BrowserEngine().init_driver()
        LoginPage(cls.driver).cookie_login()

    def setUp(self):
        self.driver.refresh()
        self.logger.info("转移流程")
        self.unit_y = YansglPage(self.driver)
        self.unit_fp = ZicfpPage(self.driver)
        self.user_sy = UserShouyPage(self.driver)
        self.dep_sy = DepShouyPage(self.driver)
        self.unit_sy = ShouyPage(self.driver)
        self.user_zy = UserZhuanyPage(self.driver)
        self.dep_zy = DepZiczyPage(self.driver)
        self.unit_zy = ZiczyPage(self.driver)
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

    #单位转移资产至部门-部门收货
    def test_danw_zhuany_bum_shouh(self):
        self.unit_sy.apply_business("申请转移")
        self.driver.refresh()
        self.unit_zy.zhuany("部门")
        success = self.dep_sy.receipt()
        self.assertTrue(success, "收货成功")

    #单位转移资产至使用人-使用人收货
    def test_danw_zhuany_shiyr_shouh(self):
        self.unit_sy.apply_business("申请转移")
        self.unit_zy.zhuany("使用人")
        success = self.user_sy.receipt()
        self.assertTrue(success, "收货成功")

    #部门转移资产-使用人收货
    def test_bum_zhuany_shiyr_shouh(self):
        self.unit_sy.apply_business("申请转移")
        self.unit_zy.zhuany("部门")
        self.dep_sy.receipt()
        self.dep_sy.apply_business("申请转移")
        self.dep_zy.zhuany("使用人")
        success = self.user_sy.receipt()
        self.assertTrue(success, "收货成功")

    #使用人转移资产-使用人收货
    def test_shiyr_zhuany_shiyr_shouh(self):
        self.unit_sy.apply_business("申请转移")
        self.unit_zy.zhuany("使用人")
        self.user_sy.receipt()
        self.user_sy.apply_business("申请转移")
        self.user_zy.zhuany("使用人")
        self.driver.refresh()
        success = self.user_sy.receipt()
        self.assertTrue(success, "收货成功")


if __name__ == "__main__":
    file_path = os.path.join(os.getcwd() + "/report/" + "test_case.html")
    f = open(file_path, 'wb')
    suite = unittest.TestSuite()
    suite.addTest(ZhuanyCase('test_danw_zhuany_bum_shouh'))
    suite.addTest(ZhuanyCase('test_danw_zhuany_shiyr_shouh'))
    suite.addTest(ZhuanyCase('test_bum_zhuany_shiyr_shouh'))
    suite.addTest(ZhuanyCase('test_shiyr_zhuany_shiyr_shouh'))
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=f, title="全量测试报告", verbosity=2)
    runner.run(suite)
