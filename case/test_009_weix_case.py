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


class WeixCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = UserLog()
        cls.logger = cls.log.get_log()
        cls.driver = BrowserEngine().init_driver()
        LoginPage(cls.driver).cookie_login()

    def setUp(self):
        self.driver.refresh()
        self.logger.info("维修")
        self.zl = make_date(self.driver)
        self.zl.unit_suoyzc_dengz()
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

    #使用人申请维修-部门同意-费用化登账
    def test_shiyr_weix_bum_ty(self):
        self.zl.unit_fenp.fenp("使用人")  # 分配至使用人
        self.zl.user_shouy.receipt("确认收货")  # 使用人收货
        self.zl.user_shouy.apply_business("申请报修")  # 使用人申请报修
        self.zl.user_weix.weix_ss("提交申请")  # 使用人提交报修单
        success = self.zl.dep_weix.weix_ss_success("同意")  # 部门同意
        self.assertTrue(success, "操作成功")
        self.driver.refresh()
        self.zl.user_weix.weix_yans(1000)  # 使用人维修验收
        self.driver.refresh()
        success = self.zl.fin_weix.weix_dengz_success("资本化")  # 财务登账
        self.assertTrue(success, "操作成功")

    #使用人申请维修-部门不同意
    def test_shiyr_weix_bum_bty(self):
        self.zl.unit_fenp.fenp("使用人")  # 分配至使用人
        self.zl.user_shouy.receipt("确认收货")  # 使用人收货
        self.zl.user_shouy.apply_business("申请报修")  # 使用人申请报修
        self.zl.user_weix.weix_ss("提交申请")  # 使用人提交报修单
        self.driver.refresh()
        success = self.zl.dep_weix.weix_ss_success("不同意")  # 部门不同意
        self.assertTrue(success, "操作成功")

    #使用人申请维修-单位同意
    def test_shiyr_weix_bum_ss_danw_ty(self):
        self.zl.unit_fenp.fenp("使用人")  # 分配至使用人
        self.zl.user_shouy.receipt("确认收货")  # 使用人收货
        self.zl.user_shouy.apply_business("申请报修")  # 使用人申请报修
        self.zl.user_weix.weix_ss("提交申请")  # 使用人提交报修单
        self.zl.dep_weix.weix_ss("送审")  # 部门送审
        self.driver.refresh()
        self.zl.unit_weix.weix_ss("同意")  # 单位同意
        self.driver.refresh()
        self.zl.user_weix.weix_yans(1000)  # 使用人维修验收
        self.driver.refresh()
        success = self.zl.fin_weix.weix_dengz_success("资本化")  # 财务登账
        self.assertTrue(success, "操作成功")

    #使用人申请维修-单位不同意
    def test_shiyr_weix_bum_ss_danw_bty(self):
        self.zl.unit_fenp.fenp("使用人")  # 分配至使用人
        self.zl.user_shouy.receipt("确认收货")  # 使用人收货
        self.zl.user_shouy.apply_business("申请报修")  # 使用人申请报修
        self.zl.user_weix.weix_ss("提交申请")  # 使用人提交报修单
        self.zl.dep_weix.weix_ss("送审")  # 部门送审
        self.driver.refresh()
        success = self.zl.unit_weix.weix_ss_success("不同意")  # 单位不同意
        self.assertTrue(success, "操作成功")

    #部门申请维修-单位同意
    def test_bum_ss_danw_ty(self):
        self.zl.unit_fenp.fenp("部门")  # 分配至部门
        self.zl.dep_shouy.receipt("确认收货")  # 部门收货
        self.zl.dep_shouy.apply_business("申请报修")  # 部门申请报修
        self.driver.refresh()
        self.zl.dep_weix.weix_ss("送审")  # 部门送审
        self.driver.refresh()
        self.zl.unit_weix.weix_ss("同意")  # 单位同意
        self.driver.refresh()
        self.zl.dep_weix.weix_yans(1000)  # 部门验收
        self.driver.refresh()
        success = self.zl.fin_weix.weix_dengz_success("资本化")  # 财务登账
        self.assertTrue(success, "操作成功")

    #单位申请维修-单位同意
    def test_danw_faq_danw_ty(self):
        self.zl.unit_shouy.apply_business("申请报修")  # 单位申请报修
        self.zl.unit_weix.weix_ss("同意")
        self.driver.refresh()
        self.zl.unit_weix.weix_yans(1000)  # 单位验收
        self.driver.refresh()
        success = self.zl.fin_weix.weix_dengz_success("资本化")  # 财务登账
        self.assertTrue(success, "操作成功")


if __name__ == "__main__":
    file_path = os.path.join(os.getcwd() + "/report/" + "test_case.html")
    f = open(file_path, 'wb')
    suite = unittest.TestSuite()
    suite.addTest(WeixCase('test_shiyr_weix_bum_ty'))
    suite.addTest(WeixCase('test_shiyr_weix_bum_bty'))
    suite.addTest(WeixCase('test_shiyr_weix_bum_ss_danw_ty'))
    suite.addTest(WeixCase('test_shiyr_weix_bum_ss_danw_bty'))
    suite.addTest(WeixCase('test_bum_ss_danw_ty'))
    suite.addTest(WeixCase('test_danw_faq_danw_ty'))
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=f, title="全量测试报告", verbosity=2)
    runner.run(suite)
