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


class TestUserWeixCase():
    def setup_class(self):
        self.log = UserLog()
        self.logger = self.log.get_log()
        self.driver = BrowserEngine().init_driver()
        LoginPage(self.driver).cookie_login()
        self.zl = make_date(self.driver)
        self.zl.user_suoyzc_dengz(value="1000", card_value='pc服务器')

    def setup(self):
        self.logger.info("维修")

    def teardown(self):
        self.driver.refresh()

    def teardown_class(self):
        self.log.close_handle()
        time.sleep(2)
        self.driver.close()
        time.sleep(2)

    #使用人申请维修-部门同意-费用化登账
    # 资本化登账后价值增加
    def test_shiyr_weix_bum_ty(self):
        self.zl.user_shouy.apply_business("申请报修")  # 使用人申请报修
        self.driver.refresh()
        self.zl.user_weix.weix_ss("提交申请")  # 使用人提交报修单
        success = self.zl.dep_weix.weix_ss_success("同意")  # 部门同意
        assert success == True
        self.driver.refresh()
        self.zl.user_weix.weix_yans(1000)  # 使用人维修验收
        self.driver.refresh()
        success = self.zl.fin_weix.weix_dengz_success("资本化")  # 财务登账
        assert success == True
        jiaz_success = self.zl.user_shouy.get_jiaz()  # 获取卡片价值
        assert jiaz_success == "2000.00"  # 资本化登账后价值增加

    #使用人申请维修-部门不同意
    def test_shiyr_weix_bum_bty(self):
        self.zl.user_shouy.apply_business("申请报修")  # 使用人申请报修
        self.driver.refresh()
        self.zl.user_weix.weix_ss("提交申请")  # 使用人提交报修单
        self.driver.refresh()
        success = self.zl.dep_weix.weix_ss_success("不同意")  # 部门不同意
        assert success == True

    #使用人申请维修-部门送审-单位同意
    # 费用化登账后价值不增加
    def test_shiyr_weix_bum_ss_danw_ty(self):
        self.zl.user_shouy.apply_business("申请报修")  # 使用人申请报修
        self.driver.refresh()
        self.zl.user_weix.weix_ss("提交申请")  # 使用人提交报修单
        self.zl.dep_weix.weix_ss("送审")  # 部门送审
        self.driver.refresh()
        self.zl.unit_weix.weix_ss("同意")  # 单位同意
        self.driver.refresh()
        self.zl.user_weix.weix_yans(1000)  # 使用人维修验收
        self.driver.refresh()
        success = self.zl.fin_weix.weix_dengz_success("资本化")  # 财务登账
        assert success == True
        jiaz_success = self.zl.user_shouy.get_jiaz()  # 获取卡片价值
        assert jiaz_success == "3000.00"  # 费用化登账后价值不增加

    #使用人申请维修-单位不同意
    def test_shiyr_weix_bum_ss_danw_bty(self):
        self.zl.user_shouy.apply_business("申请报修")  # 使用人申请报修
        self.driver.refresh()
        self.zl.user_weix.weix_ss("提交申请")  # 使用人提交报修单
        self.zl.dep_weix.weix_ss("送审")  # 部门送审
        self.driver.refresh()
        success = self.zl.unit_weix.weix_ss_success("不同意")  # 单位不同意
        assert success == True

    # 使用人 在卡片操作栏申请报修
    # 流程中卡片发起报修
    def test_shiyr_weix_caoz_faq(self):
        self.driver.refresh()
        success = self.zl.user_shouy.apply_business_success(
            "操作_申请报修")  # 使用人 在卡片操作栏申请报修
        assert success == True
        success = self.zl.user_shouy.apply_weix_error()  # 流程中卡片发起报修
        assert success == True

    #删除维修申请
    def test_shiyr_shanc_01(self):
        success = self.zl.user_weix.weix_sahnc_success()  # 删除维修单
        assert success == True

    #业务操作删除维修申请
    def test_shiyr_shanc_02(self):
        self.zl.user_shouy.apply_business("申请报修")
        success = self.zl.user_weix.weix_yewcz_sahnc_success()  # 业务操作删除维修申请
        assert success == True

    #选择当前页删除
    def test_shiyr_shanc_03(self):
        self.zl.user_shouy.apply_business("申请报修")
        success = self.zl.user_weix.weix_dangqy_sahnc_success()  # 选择当前页删除
        assert success == True

    #添加资产成功
    def test_shiyr_add_card_success(self):
        success = self.zl.user_weix.add_assets_success()
        assert success == True

    #修改维修方式成功
    def test_shiyr_change_mode_success(self):
        success = self.zl.user_weix.change_mode_success("换货")
        assert success == True

    #修改维修原因成功
    def test_shiyr_weix_reason_success(self):
        success = self.zl.user_weix.weix_reason_success("测试维修原因")
        assert success == True


class TestDepWeixCase():
    def setup_class(self):
        self.log = UserLog()
        self.logger = self.log.get_log()
        self.driver = BrowserEngine().init_driver()
        LoginPage(self.driver).cookie_login()
        self.zl = make_date(self.driver)
        self.zl.dep_suoyzc_dengz(value="1000", card_value='pc服务器')
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

    #部门申请维修-部门同意
    # 资本化登账后价值增加
    def test_bum_faq_danw_ty(self):
        self.zl.dep_shouy.apply_business("申请报修")  # 部门申请报修
        self.zl.dep_weix.weix_ss("同意")
        self.driver.refresh()
        self.zl.dep_weix.weix_yans(1000)  # 部门验收
        self.driver.refresh()
        success = self.zl.fin_weix.weix_dengz_success("资本化")  # 财务登账
        assert success == True
        jiaz_success = self.zl.dep_shouy.get_jiaz()  # 获取卡片价值
        assert jiaz_success == "2000.00"  # 资本化登账后价值增加

    # 部门 在卡片操作栏申请报修
    # 流程中卡片发起报修
    def test_bum_weix_caoz_faq(self):
        self.driver.refresh()
        success = self.zl.dep_shouy.apply_business_success(
            "操作_申请报修")  # 部门 在卡片操作栏申请报修
        assert success == True
        success = self.zl.dep_shouy.apply_weix_error()  # 流程中卡片发起报修
        assert success == True


class TestUnitWeixCase():
    def setup_class(self):
        self.log = UserLog()
        self.logger = self.log.get_log()
        self.driver = BrowserEngine().init_driver()
        LoginPage(self.driver).cookie_login()
        self.zl = make_date(self.driver)
        self.zl.unit_suoyzc_dengz(value="1000", card_value='pc服务器')
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
        success = self.zl.fin_weix.weix_dengz_success("费用化")  # 财务登账
        assert success == True
        jiaz_success = self.zl.unit_shouy.get_jiaz()  # 获取卡片价值
        assert jiaz_success == "1000.00"  # 费用化登账后价值不增加

    # 单位 在卡片操作栏申请报修
    # 流程中卡片发起报修
    def test_unit_weix_caoz_faq(self):
        self.driver.refresh()
        success = self.zl.unit_shouy.apply_business_success(
            "操作_申请报修")  # 单位 在卡片操作栏申请报修
        assert success == True
        success = self.zl.unit_shouy.apply_weix_error()  # 流程中卡片发起报修
        assert success == True


if __name__ == "__main__":
    case_path = os.path.join(os.getcwd(), 'case_pytest')
    pytest.main([
        "-s", "-v", "-q", "--html=report_weix.html",
        case_path + "\\test_009_weix_case.py::TestUserWeixCase::test_shiyr_weix_reason_success"
    ])
