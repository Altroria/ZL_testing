#coding=utf-8
import sys
import os
import time
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


class TestDengzCase():
    def setup_class(self):
        self.log = UserLog()
        self.logger = self.log.get_log()
        self.driver = BrowserEngine().init_driver()
        LoginPage(self.driver).cookie_login()

    def setup(self):
        self.logger.info("登账")
        self.zl = make_date(self.driver)
        #前置：单位资产管理员新增未登账卡片
        self.zl.unit_suoyzc_wdengz()
        time.sleep(2)

    def teardown(self):
        self.driver.refresh()

    def tearDownClass(self):
        self.log.close_handle()
        self.driver.close()

    #送财务登账-不填发票号-财务登账
    def test_danw_dengz_butfp_caiw_dengz(self):
        self.driver.refresh()
        self.zl.unit_dengz.songcw()
        self.driver.refresh()
        success = self.zl.fin_dengz.dengz_success()
        assert success == True

    #送财务登账-填发票号-财务退回
    def test_danw_dengz_tianfp_caiw_tui(self):
        self.driver.refresh()
        self.zl.unit_dengz.songcw(1000)
        self.driver.refresh()
        success = self.zl.fin_dengz.tuih_success()
        assert success == True


if __name__ == "__main__":
    case_path = os.path.join(os.getcwd(), 'case_pytest')
    pytest.main([
        "-s", "-v", "-q", "--html=report_shengl.html",
        case_path + "\\test_004_dengz_case.py::TestDengzCase::test_danw_dengz_butfp_caiw_dengz"
    ])
