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


class TestChuzCase():
    def setup_class(self):
        self.log = UserLog()
        self.logger = self.log.get_log()
        self.driver = BrowserEngine().init_driver()
        LoginPage(self.driver).cookie_login()

    def setup(self):
        self.logger.info("出租")
        self.zl = make_date(self.driver)
        self.zl.unit_suoyzc_dengz()
        self.zl.handle.refresh_f5()

    def teardown(self):
        self.driver.refresh()

    def teardown_class(self):
        self.log.close_handle()
        time.sleep(2)
        self.driver.close()

    #单位出租
    def test_chuzu_danw_faq_danw_zhix(self):
        self.zl.unit_shouy.apply_business("申请出租")
        self.zl.unit_chuzu.chuzu_scdj()  # 生成单据
        self.zl.unit_chuzu.chuzu_ss()  # 送审
        self.zl.unit_chuzu.chuzu_zhix()  # 执行
        self.zl.unit_chuzu.chuzu_shouyi("送财务部门")
        self.zl.unit_chuzu.chuzu_shouh()
        success = self.zl.fin_shouy.shouy_dengz_success()
        assert success == True


if __name__ == "__main__":
    case_path = os.path.join(os.getcwd(), 'case_pytest')
    pytest.main([
        "-s", "-v", "-q", "--html=report_chuzu.html",
        case_path + "\\test_010_chuzu_case.py::TestChuzCase"
    ])