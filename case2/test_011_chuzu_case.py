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
#单位：登账管理
from page.Unit.unit_dengzgl_page import DengzglPage
#财务：新增资产
from page.Financial.fin_xinzzc_page import XinzzcPage
#单位：所有资产-待收货
from page.Unit.unit_shouy_page import ShouyPage
#单位：资产租赁
from page.Unit.unit_chuzu_page import ChuzPage
#财务：收益管理
from page.Financial.fin_shouy_page import ShouyiPage


class ChuzCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = UserLog()
        cls.logger = cls.log.get_log()
        cls.driver = BrowserEngine().init_driver()
        LoginPage(cls.driver).cookie_login()

    def setUp(self):
        self.driver.refresh()
        self.logger.info("登账")
        self.unit_y = YansglPage(self.driver)
        self.unit_d = DengzglPage(self.driver)
        self.fin = XinzzcPage(self.driver)
        self.unit_sy = ShouyPage(self.driver)
        self.unit_cz = ChuzPage(self.driver)
        self.fin_sy = ShouyiPage(self.driver)
        #前置：单位资产管理员新增验收卡片、点击验收通过、财务登账
        self.unit_y.add_card()
        self.unit_y.start_acceptance()
        self.unit_y.yansgl_pass()
        self.unit_d.songcw(1000)
        self.fin.dengz()
        self.driver.refresh()

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
        self.unit_sy.apply_business("申请出租")
        self.unit_cz.chuzu_scdj()
        self.unit_cz.chuzu_ss()
        self.unit_cz.chuzu_tg()
        self.unit_cz.chuzu_zhix()
        self.unit_cz.chuzu_shouyi("送财务部门")
        self.unit_cz.chuzu_shouh()
        success = self.fin_sy.shouy_dengz()
        self.assertTrue(success, "收益登账成功")


if __name__ == "__main__":
    file_path = os.path.join(os.getcwd() + "/report/" + "test_case.html")
    f = open(file_path, 'wb')
    suite = unittest.TestSuite()
    suite.addTest(ChuzCase('test_chuz_danw_faq_danw_zhix'))

    runner = HTMLTestRunner.HTMLTestRunner(
        stream=f, title="全量测试报告", verbosity=2)
    runner.run(suite)
