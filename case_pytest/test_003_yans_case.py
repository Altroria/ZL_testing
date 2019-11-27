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


class TestYansglCase():
    def setup_class(self):
        self.log = UserLog()
        self.logger = self.log.get_log()
        self.driver = BrowserEngine().init_driver()
        LoginPage(self.driver).cookie_login()

    def setup(self):
        self.logger.info("验收")
        self.zl = make_date(self.driver)

    def teardown(self):
        self.driver.refresh()

    def teardown_class(self):
        self.log.close_handle()
        time.sleep(2)
        self.driver.close()

    #部门新增资产
    def test_bum_add_new_card(self):
        self.zl.dep_yans.add_card(value="1000", card_value="PC服务器")
        self.zl.dep_yans.start_acceptance()
        success = self.zl.dep_yans.yansgl_pass_success()
        assert success == True

    #部门新增同类型资产
    def test_bum_add_card(self):
        self.zl.dep_yans.add_card(value="1000")
        self.zl.dep_yans.start_acceptance()
        success = self.zl.dep_yans.yansgl_pass_success()
        assert success == True

    #单位新增资产
    def test_danw_add_new_card(self):
        self.zl.unit_yans.add_card(value="1000", card_value="PC服务器")
        self.zl.unit_yans.start_acceptance()
        self.driver.refresh()
        success = self.zl.unit_yans.yansgl_pass_success()
        assert success == True

    #单位新增同类型资产
    def test_danw_add_card(self):
        self.zl.unit_yans.add_card(value="1000", card_value="PC服务器")
        self.zl.unit_yans.start_acceptance()
        self.driver.refresh()
        success = self.zl.unit_yans.yansgl_pass_success()
        assert success == True


if __name__ == "__main__":
    case_path = os.path.join(os.getcwd(), 'case_pytest')
    pytest.main([
        "-s", "-v", "-q", "--html=report_yans.html",
        case_path + "\\test_003_yans_case.py::TestYansglCase"
    ])
