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


class ChuzCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = UserLog()
        cls.logger = cls.log.get_log()
        cls.driver = BrowserEngine().init_driver()
        LoginPage(cls.driver).cookie_login()

    def setUp(self):
        self.driver.refresh()
        self.logger.info("出租")
        self.zl = make_date(self.driver)
        self.zl.unit_suoyzc_dengz()

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

    #单位出租
    def test_chuz_danw_faq_danw_zhix(self):
        self.zl.unit_shouy.apply_business("申请出租")
        self.zl.unit_chuzu.chuzu_scdj()
        self.zl.unit_chuzu.chuzu_zhix()
        self.zl.unit_chuzu.chuzu_shouyi("送财务部门")
        self.zl.unit_chuzu.chuzu_shouh()
        success = self.zl.fin_shouy.shouy_dengz()
        self.assertTrue(success, "收益登账成功")


if __name__ == "__main__":
    file_path = os.path.join(os.getcwd() + "/report/" + "test_case.html")
    f = open(file_path, 'wb')
    suite = unittest.TestSuite()
    suite.addTest(ChuzCase('test_chuz_danw_faq_danw_zhix'))
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=f, title="全量测试报告", verbosity=2)
    runner.run(suite)