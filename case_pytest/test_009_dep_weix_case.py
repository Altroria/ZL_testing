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
        self.zl.unit_fenp.fenp("部门")  # 分配至使用人
        self.zl.user_shouy.receipt("确认收货")  # 使用人收货

    def setup(self):
        self.logger.info("维修")

    def teardown(self):
        self.driver.refresh()

    def teardown_class(self):
        self.log.close_handle()
        time.sleep(2)
        self.driver.close()
        time.sleep(2)

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


if __name__ == "__main__":
    case_path = os.path.join(os.getcwd(), 'case_pytest')
    pytest.main([
        "-s", "-v", "-q", "--html=report_weix.html", case_path +
        "\\test_009_dep_weix_case.py::TestWeixCase::test_shiyr_weix_bum_ty"
    ])
