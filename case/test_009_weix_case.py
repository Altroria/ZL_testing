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
#使用人：我要报修
from page.User.user_weix_page import UserWeixPage
#部门：维修管理
from page.Departmental.dep_weixgl_page import DepWeixglPage
#单位：维修管理
from page.Unit.unit_weixgl_page import WeixglPage
#财务：资产维修
from page.Financial.fin_weix_page import FinWeixPage


class WeixCase(unittest.TestCase):
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
        self.Dep_fp = DepZicfpPage(self.driver)
        self.unit_fp = ZicfpPage(self.driver)
        self.user_sy = UserShouyPage(self.driver)
        self.dep_sy = DepShouyPage(self.driver)
        self.unit_sy = ShouyPage(self.driver)
        self.user_weix = UserWeixPage(self.driver)
        self.dep_weix = DepWeixglPage(self.driver)
        self.unit_weix = WeixglPage(self.driver)
        self.fin_weix = FinWeixPage(self.driver)
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

    #使用人申请维修-部门同意-费用化登账
    def test_shiyr_weix_bum_ty(self):
        self.unit_fp.fenp("使用人")
        self.user_sy.receipt()
        self.user_sy.apply_business("申请报修")
        self.user_weix.weix_ss("提交申请")
        success = self.dep_weix.weix_ss("同意")
        self.assertTrue(success, "操作成功")
        self.driver.refresh()
        self.user_weix.weix_yans(1000)
        success = self.fin_weix.weix_dengz("费用化")
        self.assertTrue(success, "操作成功")

    #使用人申请维修-部门不同意
    def test_shiyr_weix_bum_bty(self):
        self.unit_fp.fenp("使用人")
        self.user_sy.receipt()
        self.user_sy.apply_business("申请报修")
        self.user_weix.weix_ss("提交申请")
        success = self.dep_weix.weix_ss("不同意")
        self.assertTrue(success, "操作成功")

    #使用人申请维修-单位同意
    def test_shiyr_weix_bum_ss_danw_ty(self):
        self.unit_fp.fenp("使用人")
        self.user_sy.receipt()
        self.user_sy.apply_business("申请报修")
        self.user_weix.weix_ss("提交申请")
        self.dep_weix.weix_ss("送审")
        self.unit_weix.weix_ss("同意")
        self.driver.refresh()
        self.driver.refresh()
        self.user_weix.weix_yans(1000)
        success = self.fin_weix.weix_dengz("资本化")
        self.assertTrue(success, "操作成功")

    #使用人申请维修-单位不同意
    def test_shiyr_weix_bum_ss_danw_bty(self):
        self.unit_fp.fenp("使用人")
        self.user_sy.receipt()
        self.user_sy.apply_business("申请报修")
        self.user_weix.weix_ss("提交申请")
        self.dep_weix.weix_ss("送审")
        success = self.unit_weix.weix_ss("不同意")
        self.assertTrue(success, "操作成功")

    #部门申请维修-单位同意
    def test_bum_ss_danw_ty(self):
        self.unit_fp.fenp("部门")
        self.dep_sy.receipt()
        self.dep_sy.apply_business("申请报修")
        self.driver.refresh()
        self.dep_weix.weix_ss("送审")
        self.unit_weix.weix_ss("同意")
        self.driver.refresh()
        self.unit_weix.weix_yans(1000)
        success = self.fin_weix.weix_dengz("费用化")
        self.assertTrue(success, "操作成功")

    #单位申请维修-单位同意
    def test_danw_faq_danw_ty(self):
        self.unit_sy.apply_business("申请报修")
        self.unit_weix.weix_ss("同意")
        self.driver.refresh()
        self.unit_weix.weix_yans(1000)
        success = self.fin_weix.weix_dengz("资本化")
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