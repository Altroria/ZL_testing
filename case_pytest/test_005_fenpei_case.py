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


class TestFenpCase():
    def setup_class(self):
        self.log = UserLog()
        self.logger = self.log.get_log()
        self.driver = BrowserEngine().init_driver()
        LoginPage(self.driver).cookie_login()

    #前置
    def setup(self):
        self.logger.info("分配")
        self.zl = make_date(self.driver)
        self.zl.unit_suoyzc_wdengz()

    def teardown(self):
        self.driver.refresh()

    def teardown_class(self):
        self.log.close_handle()
        self.driver.close()

    #单位分配资产至部门
    def test_danw_fp_bum_shouh(self):
        self.zl.unit_fenp.fenp("部门")
        #检测点：部门收货
        success = self.zl.dep_shouy.receipt_success()
        assert success == True

    #单位分配资产至使用人
    def test_danw_fp_shiyr_shouh(self):
        self.zl.unit_fenp.fenp("使用人")
        #检测点：使用人收货
        success = self.zl.user_shouy.receipt_success("确认收货")
        assert success == True

    #部门分配资产
    def test_bum_fp_bum_shouh(self):
        self.zl.unit_fenp.fenp("部门")
        self.zl.dep_shouy.receipt("确认收货")
        self.zl.dep_fenp.fenp("使用人")
        #检测点：使用人收货
        success = self.zl.user_shouy.receipt_success("确认收货")
        assert success == True


if __name__ == "__main__":
    case_path = os.path.join(os.getcwd(), 'case_pytest')
    pytest.main([
        "-s", "-v", "-q", "--html=report_fenpei.html",
        case_path + "\\test_005_fenpei_case.py::TestFenpCase"
    ])
