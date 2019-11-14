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

    #使用人归还-部门收货
    def test_shiyr_guih_bum_shouh(self):
        self.zl.unit_fenp.fenp("使用人")
        self.zl.user_shouy.receipt()
        self.zl.user_guih.guih_pass()
        #检查点：部门收货归还的卡片
        success = self.zl.dep_shouy.receipt()
        self.assertTrue(success, "收货成功")

    #部门归还-单位收货
    def test_bum_guih_danw_shouh(self):
        self.zl.unit_fenp.fenp("部门")
        self.zl.dep_shouy.receipt()
        self.zl.dep_guih.guih_pass()
        #检查点：单位收货归还的卡片
        success = self.zl.unit_shouy.receipt()
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
