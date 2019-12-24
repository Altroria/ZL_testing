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


class TestZhuanyCase():
    def setup_class(self):
        self.log = UserLog()
        self.logger = self.log.get_log()
        self.driver = BrowserEngine().init_driver()
        LoginPage(self.driver).cookie_login()

    def setup(self):
        self.logger.info("转移流程")
        self.zl = make_date(self.driver)
        self.zl.unit_suoyzc_wdengz()

    def teardown(self):
        self.driver.refresh()

    def teardown_class(self):
        time.sleep(2)
        self.log.close_handle()
        time.sleep(2)
        self.driver.close()
        time.sleep(2)

    #单位转移资产至部门-部门收货
    def test_danw_zhuany_bum_shouh(self):
        self.zl.unit_shouy.apply_business("申请转移")
        self.zl.unit_zhuany.zhuany("部门")
        #检查点：部门收货单位转移的资产
        success = self.zl.dep_shouy.receipt_success()
        assert success == True

    #单位转移资产至使用人-使用人收货
    def test_danw_zhuany_shiyr_shouh(self):
        self.zl.unit_shouy.apply_business("申请转移")
        self.zl.unit_zhuany.zhuany("使用人")
        #检查点：使用人收货单位转移的资产
        success = self.zl.user_shouy.receipt_success("确认收货")
        assert success == True

    #部门转移资产-使用人收货
    def test_bum_zhuany_shiyr_shouh(self):
        self.zl.unit_shouy.apply_business("申请转移")
        self.zl.unit_zhuany.zhuany("部门")
        self.zl.dep_shouy.receipt("确认收货")
        self.zl.dep_shouy.apply_business("申请转移")
        self.zl.dep_zhuany.zhuany("使用人")
        #检查点：使用人收货部门转移的资产
        success = self.zl.user_shouy.receipt_success("确认收货")
        assert success == True

    #使用人转移资产-使用人收货
    def test_shiyr_zhuany_shiyr_shouh(self):
        self.zl.unit_shouy.apply_business("申请转移")
        self.zl.unit_zhuany.zhuany("使用人")
        self.zl.handle.refresh_f5()
        self.zl.user_shouy.receipt("确认收货")
        self.zl.user_shouy.apply_business("申请转移")
        self.zl.user_zhuany.zhuany("使用人")
        #检查点：使用人收货使用人转移的资产
        self.zl.handle.refresh_f5()
        success = self.zl.user_shouy.receipt_success("确认收货")
        assert success == True


if __name__ == "__main__":
    case_path = os.path.join(os.getcwd(), 'case_pytest')
    pytest.main([
        "-s", "-v", "-q", "--html=report_zhuanyi.html",
        case_path + "\\test_007_zhuanyi_case.py::TestZhuanyCase::test_bum_zhuany_shiyr_shouh"
    ])
