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
        time.sleep(2)

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

    #单位出借
    def test_chujie_danw_faq_danw_zhix(self):
        self.zl.unit_shouy.apply_business("申请出借")
        self.zl.unit_chuzu.chuzu_scdj()  # 生成单据
        self.zl.unit_chuzu.chuzu_ss()  # 送审
        self.zl.unit_chuzu.chuzu_zhix()  # 执行
        self.zl.unit_chuzu.chuzu_shouyi("送财务部门")
        self.zl.unit_chuzu.chuzu_shouh()
        success = self.zl.fin_shouy.shouy_dengz_success()
        assert success == True

    #添加资产
    #出租
    def test_addcard_chuz(self):
        success = self.zl.unit_chuzu.chuzu_addcard_success("出租")
        assert success == True
        success = self.zl.unit_chuzu.quxiao_success()
        assert success == True

    #添加资产
    #出借
    def test_addcard_chuj(self):
        success = self.zl.unit_chuzu.chuzu_addcard_success("出借")
        assert success == True
        success = self.zl.unit_chuzu.quxiao_success()
        assert success == True

    #操作栏取消单据
    def test_caoz_qux(self):
        success = self.zl.unit_chuzu.chuzu_addcard_success("出租")
        assert success == True
        success = self.zl.unit_chuzu.caoz_qux_success()
        assert success == True

    #操作栏生成单据
    def test_caoz_scdj(self):
        success = self.zl.unit_chuzu.chuzu_addcard_success("出借")
        assert success == True
        success = self.zl.unit_chuzu.caoz_scdj_success()
        assert success == True

    #待送审-修改
    def test_chuzu_xiug(self):
        success = self.zl.unit_chuzu.chuzu_xiug_success()
        assert success == True

    #待送审-删除
    def test_chuzu_del(self):
        success = self.zl.unit_chuzu.chuzu_del_success()
        assert success == True


if __name__ == "__main__":
    case_path = os.path.join(os.getcwd(), 'case_pytest')
    pytest.main([
        "-s", "-v", "-q", "--html=report_chuzu.html",
        case_path + "\\test_010_chuzu_case.py"
    ])
