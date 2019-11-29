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


class TestGuihCase():
    def setup_class(self):
        self.log = UserLog()
        self.logger = self.log.get_log()
        self.driver = BrowserEngine().init_driver()
        LoginPage(self.driver).cookie_login()

    def setup(self):
        self.logger.info("归还")
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

    #使用人归还-部门收货
    def test_shiyr_guih_bum_shouh(self):
        self.zl.unit_fenp.fenp("使用人")
        self.zl.user_shouy.receipt("确认收货")
        self.zl.user_guih.guih_pass()
        #检查点：部门收货归还的卡片
        success = self.zl.dep_shouy.receipt_success()
        assert success == True

    #部门归还-单位收货
    def test_bum_guih_danw_shouh(self):
        self.zl.unit_fenp.fenp("部门")
        self.zl.dep_shouy.receipt("确认收货")
        self.zl.dep_guih.guih_pass()
        #检查点：单位收货归还的卡片
        success = self.zl.unit_shouy.receipt_success()
        assert success == True


if __name__ == "__main__":
    case_path = os.path.join(os.getcwd(), 'case_pytest')

    pytest.main([
        "-s", "-v", "-q", "--html=report_guihuan.html",
        case_path + "\\test_006_guihuan_case.py::TestGuihCase"
    ])
