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

    #单位转移资产至部门-部门收货
    def test_danw_zhuany_bum_shouh(self):
        self.zl.unit_shouy.apply_business("申请转移")
        self.zl.unit_zhuany.zhuany("部门")
        #检查点：部门收货单位转移的资产
        success = self.zl.dep_shouy.receipt()
        self.assertTrue(success, "收货成功")

    #单位转移资产至使用人-使用人收货
    def test_danw_zhuany_shiyr_shouh(self):
        self.zl.unit_shouy.apply_business("申请转移")
        self.zl.unit_zhuany.zhuany("使用人")
        #检查点：使用人收货单位转移的资产
        success = self.zl.user_shouy.receipt()
        self.assertTrue(success, "收货成功")

    #部门转移资产-使用人收货
    def test_bum_zhuany_shiyr_shouh(self):
        self.zl.unit_shouy.apply_business("申请转移")
        self.zl.unit_zhuany.zhuany("部门")
        self.zl.dep_shouy.receipt()
        self.zl.dep_shouy.apply_business("申请转移")
        self.zl.dep_zhuany.zhuany("使用人")
        #检查点：使用人收货部门转移的资产
        success = self.zl.user_shouy.receipt()
        self.assertTrue(success, "收货成功")

    #使用人转移资产-使用人收货
    def test_shiyr_zhuany_shiyr_shouh(self):
        self.zl.unit_shouy.apply_business("申请转移")
        self.zl.unit_zhuany.zhuany("使用人")
        self.zl.user_shouy.receipt()
        self.zl.user_shouy.apply_business("申请转移")
        self.zl.user_zhuany.zhuany("使用人")
        #检查点：使用人收货使用人转移的资产
        self.zl.handle.refresh_f5()
        success = self.zl.user_shouy.receipt()
        self.assertTrue(success, "收货成功")


if __name__ == "__main__":
    file_path = os.path.join(os.getcwd() + "/report/" + "test_case.html")
    f = open(file_path, 'wb')
    suite = unittest.TestSuite()
    #suite.addTest(ZhuanyCase('test_danw_zhuany_bum_shouh'))
    #suite.addTest(ZhuanyCase('test_danw_zhuany_shiyr_shouh'))
    #suite.addTest(ZhuanyCase('test_bum_zhuany_shiyr_shouh'))
    suite.addTest(ZhuanyCase('test_shiyr_zhuany_shiyr_shouh'))
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=f, title="全量测试报告", verbosity=2)
    runner.run(suite)
