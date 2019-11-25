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

    #部门收回卡片
    def test_bum_shouh(self):
        self.zl.unit_fenp.fenp("使用人")  # 单位分配给使用人
        self.zl.dep_shouy.receipt("确认收货")  # 部门收货
        self.driver.refresh()
        #检测点：部门收回卡片成功
        success = self.zl.dep_shouh.take_back_success()
        self.assertTrue(success, "收回成功")

    #部门全部收回卡片
    def test_bum_shouh_all(self):
        self.zl.unit_fenp.fenp("使用人")  # 单位分配给使用人
        self.zl.dep_shouy.receipt("确认收货")  # 部门收货
        self.driver.refresh()
        #检查点：部门全部收回卡片成功
        success = self.zl.dep_shouh.all_take_back_success()
        self.assertTrue(success, "收回成功")

    #单位收回卡片
    def test_danw_shouh(self):
        self.zl.unit_fenp.fenp("使用人")
        self.zl.unit_shouy.receipt("确认收货")
        self.driver.refresh()
        #检查点：单位收回卡片成功
        success = self.zl.unit_shouh.take_back_success()
        self.assertTrue(success, "收回成功")

    #单位全部收回卡片
    def test_danw_shouh_all(self):
        self.zl.unit_fenp.fenp("使用人")  # 分配至使用人
        self.zl.user_shouy.receipt("确认收货")  # 使用人收货
        self.driver.refresh()
        #检查点：单位全部收回卡片成功
        success = self.zl.unit_shouh.all_take_back_success()  # 单位收回
        self.assertTrue(success, "收回成功")


if __name__ == "__main__":
    file_path = os.path.join(os.getcwd() + "/report/" + "test_case.html")
    f = open(file_path, 'wb')
    suite = unittest.TestSuite()
    suite.addTest(ShouhCase('test_bum_shouh'))
    suite.addTest(ShouhCase('test_bum_shouh_all'))
    suite.addTest(ShouhCase('test_danw_shouh'))
    #suite.addTest(ShouhCase('test_danw_shouh_all'))
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=f, title="全量测试报告", verbosity=2)
    runner.run(suite)
