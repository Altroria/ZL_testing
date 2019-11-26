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


class Testchengzu():
    def setup_class(self):
        self.log = UserLog()
        self.logger = self.log.get_log()
        self.driver = BrowserEngine().init_driver()
        LoginPage(self.driver).cookie_login()

    def setup(self):
        self.logger.info("出租")
        self.zl = make_date(self.driver)

    def teardown(self):
        self.driver.refresh()

    def teardown_sclass(self):
        self.log.close_handle()
        self.driver.close()

    #承租——续租
    def test_chenz_xvzu_01(self):
        self.zl.unit_chengzu.xinz()
        self.zl.unit_chengzu.jiaofu()
        success = self.zl.unit_chengzu.xvzu_success()
        assert success == True

    #承租——退还
    def test_chenz_tuihuan_01(self):
        self.zl.unit_chengzu.xinz()
        self.zl.unit_chengzu.jiaofu()
        success = self.zl.unit_chengzu.tuih_success()
        assert success == True
        #承租完成的再次续租
        self.zl.handle.refresh_f5()
        success = self.zl.unit_chengzu.zaicxz_success()
        assert success == True

    #承租——批量退还
    def test_chenz_tuihuan_02(self):
        self.zl.unit_chengzu.xinz()
        self.zl.unit_chengzu.jiaofu()
        success = self.zl.unit_chengzu.pilth()
        assert success == True


if __name__ == "__main__":
    case_path = os.path.join(os.getcwd(), 'case_pytest')
    '''
    pytest.main([
        "-s", "-v", "-q",
        case_path + "\\test_002_shenl_case.py::Testchengzu::test_shiyr_sl_bum_th",
        case_path + "\\test_002_shenl_case.py::Testchengzu::test_shiyr_sl_bum_ty",
        case_path + "\\test_002_shenl_case.py::Testchengzu::test_shiyr_sl_bum_bty",
        case_path + "\\test_002_shenl_case.py::Testchengzu::test_shiyr_sl_bum_ss_danw_th",
        case_path + "\\test_002_shenl_case.py::Testchengzu::test_shiyr_sl_bum_ss_danw_ty",
        case_path + "\\test_002_shenl_case.py::Testchengzu::test_shiyr_sl_bum_ss_danw_bty",
        case_path + "\\test_002_shenl_case.py::Testchengzu::test_bum_sl_danw_ty"
    ])
    '''
    pytest.main([
        "-s", "-v", "-q", "--html=report_shengl.html",
        case_path + "\\test_002_shenl_case.py::Testchengzu"
    ])
