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


class TestWeixCase():
    def setup_class(self):
        self.log = UserLog()
        self.logger = self.log.get_log()
        self.driver = BrowserEngine().init_driver()
        LoginPage(self.driver).cookie_login()
        self.zl = make_date(self.driver)
        self.zl.unit_suoyzc_dengz()
        self.driver.refresh()

    def setup(self):
        self.logger.info("维修")

    def teardown(self):
        self.driver.refresh()

    def teardown_class(self):
        self.log.close_handle()
        time.sleep(2)
        self.driver.close()
        time.sleep(2)

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
    pytest.main([
        "-s", "-v", "-q", "--html=report_weix.html", case_path +
        "\\test_009_unit_weix_case.py::TestWeixCase::test_shiyr_weix_bum_ty"
    ])
