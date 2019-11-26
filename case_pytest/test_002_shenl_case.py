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


class TestShenlCase():
    def setup_class(self):
        self.log = UserLog()
        self.logger = self.log.get_log()
        self.driver = BrowserEngine().init_driver()
        LoginPage(self.driver).cookie_login()

    def setup(self):
        self.logger.info("配置管理")
        self.zl = make_date(self.driver)

    def teardown(self):
        self.driver.refresh()

    def teardown_class(self):
        self.log.close_handle()
        self.driver.close()

    #使用人申领-部门退回
    def test_shiyr_sl_bum_th(self):
        self.zl.user_shenl.shenl_xinz("PC服务器")
        self.zl.user_shenl.shenl_tj()
        success = self.zl.dep_peiz.peiz_ss_success("退回")
        assert success == True

    #使用人申领-部门同意
    def test_shiyr_sl_bum_ty(self):
        self.zl.user_shenl.shenl_xinz("PC服务器")
        self.zl.user_shenl.shenl_tj()
        success = self.zl.dep_peiz.peiz_ss_success("同意")
        assert success == True

    #使用人申领-部门不同意
    def test_shiyr_sl_bum_bty(self):
        self.zl.user_shenl.shenl_xinz("PC服务器")
        self.zl.user_shenl.shenl_tj()
        success = self.zl.dep_peiz.peiz_ss_success("同意")
        assert success == True

    #使用人申领-部门送审-单位退回
    def test_shiyr_sl_bum_ss_danw_th(self):
        self.zl.user_shenl.shenl_xinz("PC服务器")
        self.zl.user_shenl.shenl_tj()
        self.zl.dep_peiz.peiz_ss("送审")
        self.driver.refresh()
        success = self.zl.unit_peiz.peiz_ss_success("退回")
        assert success == True

    #使用人申领-部门送审-单位同意
    def test_shiyr_sl_bum_ss_danw_ty(self):
        self.zl.user_shenl.shenl_xinz("PC服务器")
        self.zl.user_shenl.shenl_tj()
        self.zl.dep_peiz.peiz_ss("送审")
        self.driver.refresh()
        success = self.zl.unit_peiz.peiz_ss_success("同意")
        assert success == True

    #使用人申领-部门送审-单位不同意
    def test_shiyr_sl_bum_ss_danw_bty(self):
        self.zl.user_shenl.shenl_xinz("PC服务器")
        self.zl.user_shenl.shenl_tj()
        self.zl.dep_peiz.peiz_ss("送审")
        self.driver.refresh()
        success = self.zl.unit_peiz.peiz_ss_success("不同意")
        assert success == True

    #部门申领-单位同意
    def test_bum_sl_danw_ty(self):
        self.zl.dep_peiz.peiz_tj("PC服务器")
        self.driver.refresh()
        self.zl.dep_peiz.peiz_ss("送审")
        self.driver.refresh()
        success = self.zl.unit_peiz.peiz_ss_success("同意")
        assert success == True


if __name__ == "__main__":
    case_path = os.path.join(os.getcwd(), 'case_pytest')
    '''
    pytest.main([
        "-s", "-v", "-q",
        case_path + "\\test_002_shenl_case.py::TestShenlCase::test_shiyr_sl_bum_th",
        case_path + "\\test_002_shenl_case.py::TestShenlCase::test_shiyr_sl_bum_ty",
        case_path + "\\test_002_shenl_case.py::TestShenlCase::test_shiyr_sl_bum_bty",
        case_path + "\\test_002_shenl_case.py::TestShenlCase::test_shiyr_sl_bum_ss_danw_th",
        case_path + "\\test_002_shenl_case.py::TestShenlCase::test_shiyr_sl_bum_ss_danw_ty",
        case_path + "\\test_002_shenl_case.py::TestShenlCase::test_shiyr_sl_bum_ss_danw_bty",
        case_path + "\\test_002_shenl_case.py::TestShenlCase::test_bum_sl_danw_ty"
    ])
    '''
    pytest.main([
        "-s",
        "-v",
        "-q",
        "--html=report_shengl.html",
        case_path + "\\test_002_shenl_case.py::TestShenlCase::test_shiyr_sl_bum_th"
    ])
