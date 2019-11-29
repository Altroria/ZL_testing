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


class TestShouhCase():
    def setup_class(self):
        self.log = UserLog()
        self.logger = self.log.get_log()
        self.driver = BrowserEngine().init_driver()
        LoginPage(self.driver).cookie_login()

    def setup(self):
        self.logger.info("收回")
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

    #部门收回卡片
    def test_bum_shouh(self):
        self.zl.unit_fenp.fenp("使用人")  # 单位分配给使用人
        self.zl.dep_shouy.receipt("确认收货")  # 部门收货
        self.driver.refresh()
        #检测点：部门收回卡片成功
        success = self.zl.dep_shouh.take_back_success()
        assert success == True

    #部门全部收回卡片
    def test_bum_shouh_all(self):
        self.zl.unit_fenp.fenp("使用人")  # 单位分配给使用人
        self.zl.dep_shouy.receipt("确认收货")  # 部门收货
        self.driver.refresh()
        #检查点：部门全部收回卡片成功
        success = self.zl.dep_shouh.all_take_back_success()
        assert success == True

    #单位收回卡片
    def test_danw_shouh(self):
        self.zl.unit_fenp.fenp("使用人")
        self.zl.unit_shouy.receipt("确认收货")
        self.driver.refresh()
        #检查点：单位收回卡片成功
        success = self.zl.unit_shouh.take_back_success()
        assert success == True

    #单位全部收回卡片
    def test_danw_shouh_all(self):
        self.zl.unit_fenp.fenp("使用人")  # 分配至使用人
        self.zl.user_shouy.receipt("确认收货")  # 使用人收货
        self.driver.refresh()
        #检查点：单位全部收回卡片成功
        success = self.zl.unit_shouh.all_take_back_success()  # 单位收回
        assert success == True


if __name__ == "__main__":
    case_path = os.path.join(os.getcwd(), 'case_pytest')
    pytest.main([
        "-s", "-v", "-q", "--html=report_shouhui.html",
        case_path + "\\test_008_shouhui_case.py::TestShouhCase::test_bum_shouh"
    ])
