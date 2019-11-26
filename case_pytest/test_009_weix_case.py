#coding=utf-8
import sys
import os
import pytest
sys.path.append(os.path.join(os.getcwd()))
#初始driver
from base.browser_engine import BrowserEngine
#日志
from log.user_log import UserLog
#登陆
from page.login_page import LoginPage
#数据初始 + 检测点模块
from page.date.make_date import make_date


class TestWeixCase():
    def setup_class(self):
        self.log = UserLog()
        self.logger = self.log.get_log()
        self.driver = BrowserEngine().init_driver()
        LoginPage(self.driver).cookie_login()

    def setup(self):
        self.logger.info("维修")
        self.zl = make_date(self.driver)
        self.zl.unit_suoyzc_dengz()
        self.driver.refresh()

    def teardown(self):
        self.driver.refresh()

    def teardown_class(self):
        self.log.close_handle()
        self.driver.close()

    #使用人申请维修-部门同意-费用化登账
    def test_shiyr_weix_bum_ty(self):
        self.zl.unit_fenp.fenp("使用人")  # 分配至使用人
        self.zl.user_shouy.receipt("确认收货")  # 使用人收货
        self.zl.user_shouy.apply_business("申请报修")  # 使用人申请报修
        self.zl.user_weix.weix_ss("提交申请")  # 使用人提交报修单
        success = self.zl.dep_weix.weix_ss_success("同意")  # 部门同意
        assert success == True
        self.driver.refresh()
        self.zl.user_weix.weix_yans(1000)  # 使用人维修验收
        self.driver.refresh()
        success = self.zl.fin_weix.weix_dengz_success("资本化")  # 财务登账
        assert success == True

    #使用人申请维修-部门不同意
    def test_shiyr_weix_bum_bty(self):
        self.zl.unit_fenp.fenp("使用人")  # 分配至使用人
        self.zl.user_shouy.receipt("确认收货")  # 使用人收货
        self.zl.user_shouy.apply_business("申请报修")  # 使用人申请报修
        self.zl.user_weix.weix_ss("提交申请")  # 使用人提交报修单
        self.driver.refresh()
        success = self.zl.dep_weix.weix_ss_success("不同意")  # 部门不同意
        assert success == True

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
        assert success == True

    #使用人申请维修-单位不同意
    def test_shiyr_weix_bum_ss_danw_bty(self):
        self.zl.unit_fenp.fenp("使用人")  # 分配至使用人
        self.zl.user_shouy.receipt("确认收货")  # 使用人收货
        self.zl.user_shouy.apply_business("申请报修")  # 使用人申请报修
        self.zl.user_weix.weix_ss("提交申请")  # 使用人提交报修单
        self.zl.dep_weix.weix_ss("送审")  # 部门送审
        self.driver.refresh()
        success = self.zl.unit_weix.weix_ss_success("不同意")  # 单位不同意
        assert success == True

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
        assert success == True

    #单位申请维修-单位同意
    def test_danw_faq_danw_ty(self):
        self.zl.unit_shouy.apply_business("申请报修")  # 单位申请报修
        self.zl.unit_weix.weix_ss("同意")
        self.driver.refresh()
        self.zl.unit_weix.weix_yans(1000)  # 单位验收
        self.driver.refresh()
        success = self.zl.fin_weix.weix_dengz_success("资本化")  # 财务登账
        assert success == True


if __name__ == "__main__":
    case_path = os.path.join(os.getcwd(), 'case_pytest')
    '''
    pytest.main([
        "-s", "-v", "-q",
        case_path + "\\test_002_shenl_case.py::TestWeixCase::test_shiyr_sl_bum_th",
        case_path + "\\test_002_shenl_case.py::TestWeixCase::test_shiyr_sl_bum_ty",
        case_path + "\\test_002_shenl_case.py::TestWeixCase::test_shiyr_sl_bum_bty",
        case_path + "\\test_002_shenl_case.py::TestWeixCase::test_shiyr_sl_bum_ss_danw_th",
        case_path + "\\test_002_shenl_case.py::TestWeixCase::test_shiyr_sl_bum_ss_danw_ty",
        case_path + "\\test_002_shenl_case.py::TestWeixCase::test_shiyr_sl_bum_ss_danw_bty",
        case_path + "\\test_002_shenl_case.py::TestWeixCase::test_bum_sl_danw_ty"
    ])
    '''
    pytest.main([
        "-s", "-v", "-q", "--html=report_shengl.html",
        case_path + "\\test_002_shenl_case.py::TestWeixCase"
    ])
