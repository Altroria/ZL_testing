#coding=utf-8

import sys
import os
sys.path.append(os.path.join(os.getcwd()))
from selenium import webdriver

import time
from base.base_handle import BaseHandle
from page.Departmental import *
from page.Financial import *
from page.Unit import *
from page.User import *


class make_date():
    def __init__(self, driver):
        self.handle = BaseHandle(driver)
        self.unit_chengzu = unit_chengzu_page.chengzu(driver)
        self.unit_chuzu = unit_chuzu_page.ChuzPage(driver)
        self.unit_dengz = unit_dengzgl_page.DengzglPage(driver)
        self.unit_touz = unit_duiwtz_page.DuiwtzPage(driver)
        self.unit_peiz = unit_peiz_page.PeizlPage(driver)
        self.unit_shouy = unit_shouy_page.ShouyPage(driver)
        self.unit_weix = unit_weixgl_page.WeixglPage(driver)
        self.unit_yans = unit_yansgl_page.YansglPage(driver)
        self.unit_chuz = unit_ziccz_page.ZicczPage(driver)
        self.unit_fenp = unit_zicfp_page.ZicfpPage(driver)
        self.unit_shouh = unit_zicsh_page.ZicshPage(driver)
        self.unit_zhuany = unit_ziczy_page.ZiczyPage(driver)
        self.unit_shouygl = unit_shouygl_page.ShouyglPage(driver)

        self.fin_hex = fin_hexzc_page.HexzcPage(driver)
        self.fin_shouy = fin_shouy_page.ShouyiPage(driver)
        self.fin_weix = fin_weix_page.FinWeixPage(driver)
        self.fin_dengz = fin_xinzzc_page.XinzzcPage(driver)

        self.dep_guih = dep_guih_page.DepGuihPage(driver)
        self.dep_peiz = dep_peiz_page.DepPeizlPage(driver)
        self.dep_shouy = dep_shouy_page.DepShouyPage(driver)
        self.dep_weix = dep_weixgl_page.DepWeixglPage(driver)
        self.dep_yans = dep_yansgl_page.DepYansglPage(driver)
        self.dep_ziccz = dep_ziccz_page.DepZicczPage(driver)
        self.dep_fenp = dep_zicfp_page.DepZicfpPage(driver)
        self.dep_shouh = dep_zicsh_page.DepZicshPage(driver)
        self.dep_zhuany = dep_ziczy_page.DepZiczyPage(driver)

        self.user_chuz = user_chuz_page.UserZicczPage(driver)
        self.user_guih = user_guih_page.UserGuihPage(driver)
        self.user_shenl = user_shenl_page.UserShenllPage(driver)
        self.user_shouy = user_shouy_page.UserShouyPage(driver)
        self.user_zhuany = user_zhuany_page.UserZhuanyPage(driver)
        self.user_weix = user_weix_page.UserWeixPage(driver)
        self.user_yans = user_yans_page.UserYansPage(driver)

    def unit_suoyzc_wdengz(self, value="1000", card_value='pc服务器'):
        '''
        单位资产管理员验收未登账卡片
        '''
        self.unit_yans.add_card(value, card_value)
        self.unit_yans.start_acceptance()
        self.unit_yans.yansgl_pass()

    def unit_suoyzc_dengz(self):
        '''
        单位资产管理员验收登账卡片
        '''
        self.unit_suoyzc_wdengz()
        self.unit_dengz.songcw()
        self.fin_dengz.dengz()

    def unit_peiz_01(self):
        '''
        新增配置管理--待审核数据
        '''
        self.dep_peiz.peiz_tj()
        self.refresh_f5()
        self.dep_peiz.peiz_ss("送审")

    def unit_peiz_02(self, value="同意"):
        '''
        新增配置管理--已审核数据
        value：默认同意
        '''
        self.unit_peiz_01()
        self.unit_peiz.peiz_ss(value)

    def unit_yans_01(self):
        '''
        新增验管理--待验收数据
        '''
        self.unit_yans.add_card(card_value="pc服务器")

    def unit_yans_02(self):
        '''
        新增验管理--验收中数据
        '''
        self.unit_yans_01()
        self.unit_yans.start_acceptance()

    def unit_yans_03(self):
        '''
        新增验管理--验收完成数据
        '''
        self.unit_yans_02()
        self.unit_yans.yansgl_pass()

    def unit_dengz_01(self):
        '''
        新增登账管理--待登账数据
        '''
        self.unit_yans_03()

    def unit_dengz_02(self, value=None):
        '''
        新增登账管理--登账中数据
        默认无发票号
        '''
        self.unit_dengz_01()
        self.unit_dengz.songcw(value)

    def unit_dengz_03(self, value=None):
        '''
        新增登账管理--登账完成数据
        默认无发票号
        '''
        self.unit_dengz_02(value)
        self.fin_dengz.dengz()
        self.handle.refresh_f5()

    def unit_fenp_01(self):
        '''
        单位资产管理员新增资产分配--待分配
        '''
        self.unit_yans_03()

    def unit_fenp_02(self):
        '''
        单位资产管理员新增资产分配--分配中
        '''
        self.unit_fenp_01()
        self.unit_fenp.fenp("部门")

    def unit_fenp_03(self):
        '''
        单位资产管理员新增资产分配--分配完成
        '''
        self.unit_fenp_02()
        self.unit_shouy.receipt()

    def unit_shouhui_01(self):
        '''
        新增资产收回--待收回
        '''
        self.unit_fenp_03()

    def unit_shouhui_02(self):
        '''
        新增资产收回--收回完成
        '''
        self.unit_shouhui_01()
        self.unit_shouh.take_back()

    def unit_zhuany_01(self):
        '''
        新增资产转移--待转移
        '''
        self.unit_yans_03()
        self.unit_shouy.apply_business("申请转移")

    def unit_zhuany_02(self):
        '''
        新增资产转移--转移中
        '''
        self.unit_zhuany_01()
        self.unit_zhuany.zhuany("部门")

    def unit_zhuany_03(self):
        '''
        新增资产转移--转移中
        '''
        self.unit_zhuany_02()
        self.unit_shouy.receipt()

    def unit_weix_01(self):
        '''
        新增维修管理--待审核
        '''
        self.unit_dengz_03()
        self.unit_shouy.apply_business("申请报修")

    def unit_weix_02(self):
        '''
        新增维修管理--已审核
        '''
        self.unit_weix_01()
        self.unit_weix.weix_ss("同意")

    def unit_weix_03(self):
        '''
        新增维修管理--维修完成
        '''
        self.unit_weix_02()
        self.unit_weix.weix_yans(1000)

    def unit_chuz_01(self):
        '''
        新增资产处置--待审核
        '''
        self.unit_dengz_03()
        self.unit_shouy.apply_business("申请处置")

    def unit_chuz_02(self):
        '''
        新增资产处置--待审核
        '''
        self.unit_chuz_01()
        self.unit_chuz.chuz_shengcczd()

    def unit_chuz_03(self):
        '''
        新增资产处置--已审核
        '''
        self.unit_chuz_02()
        self.unit_chuz.chuz_songs()

    def unit_chuz_04(self):
        '''
        新增资产处置--执行中
        '''
        self.unit_chuz_03()
        self.unit_chuz.chuz_zhix()

    def unit_chuz_05(self):
        '''
        新增资产处置--完成
        '''
        self.unit_chuz_04()
        self.unit_chuz.chuz_chuzhi()

    def unit_chuzu_01(self):
        '''
        新增资产出租--待审核
        '''
        self.unit_dengz_03()
        self.unit_shouy.apply_business("申请出租")

    def unit_chuzu_02(self):
        '''
        新增资产出租--待送审
        '''
        self.unit_chuzu_01()
        self.unit_chuzu.chuzu_scdj()

    def unit_chuzu_03(self):
        '''
        新增资产出租-审批中
        '''
        self.unit_chuzu_02()
        self.unit_chuzu.chuzu_ss()

    def unit_chuzu_04(self):
        '''
        新增资产出租-已审批
        '''
        self.unit_chuzu_03()
        self.unit_chuzu.chuzu_tg()

    def unit_chuzu_05(self):
        '''
        新增资产出租-出租(借)中
        '''
        self.unit_chuzu_04()
        self.unit_chuzu.chuzu_zhix()

    def unit_chuzu_06(self):
        '''
        新增资产出租-租(借)收回
        '''
        self.unit_chuzu_05()
        self.unit_chuzu.chuzu_shouh()

    def unit_chengzu_01(self):
        '''
        新增承租借-待承租借
        '''
        self.unit_chengzu.xinz()

    def unit_chengzu_02(self):
        '''
        新增承租借-承租借中
        '''
        self.unit_chengzu_01()
        self.unit_chengzu.jiaofu()

    def unit_chengzu_03(self):
        '''
        新增承租借-承租借完成
        '''
        self.unit_chengzu_02()
        self.unit_chengzu.tuih()

    def unit_shouy_01(self):
        '''
        新增收益管理--待登账
        出租收益
        '''
        self.unit_chuzu_06()
        self.unit_chuzu.chuzu_shouyi("暂存")

    def unit_shouy_02(self):
        '''
        新增收益管理--登账中
        '''
        self.unit_shouy_01()
        self.refresh_f5()
        self.unit_shouygl.shouy_ss()

    def unit_shouy_03(self):
        '''
        新增收益管理--已登账
        '''
        self.unit_shouy_02()
        self.fin_shouy.shouy_dengz()

    def user_suoyzc_wdengz(self):
        '''
        使用人所有资产界面添加未登账卡片
        '''
        self.unit_suoyzc_wdengz()
        self.unit_fenp.fenp("使用人")
        self.user_shouy.receipt()

    def user_suoyzc_dengz(self):
        '''
        使用人所有资产界面添加登账卡片
        '''
        self.unit_suoyzc_dengz()
        self.unit_fenp.fenp("使用人")
        self.user_shouy.receipt()

    def user_shenl_01(self):
        '''
        使用人我要申领--待提交界面添加数据
        '''
        self.user_shenl.shenl_xinz(card_value="pc服务器")

    def user_shenl_02(self):
        '''
        使用人我要申领--审核中界面添加数据
        '''
        self.user_shenl_01()
        self.user_shenl.shenl_tj()

    def user_shenl_03(self):
        '''
        使用人我要申领--已审核界面添加数据
        '''
        self.user_shenl_02()
        self.dep_peiz.peiz_ss("同意")

    def user_baox_01(self):
        '''
        使用人我要报修--待提交界面添加数据
        '''
        self.user_suoyzc_dengz()
        self.user_shouy.apply_business("申请报修")

    def user_baox_02(self):
        '''
        使用人我要报修--审核中界面添加数据
        '''
        self.user_baox_01()
        self.user_weix.weix_ss("提交申请")

    def user_baox_03(self):
        '''
        使用人我要报修--已审核界面添加数据
        '''
        self.user_baox_02()
        self.dep_weix.weix_ss("同意")

    def user_baox_04(self):
        '''
        使用人我要报修--维修完成界面添加数据
        '''
        self.user_baox_03()
        self.dep_weix.weix_yans(1000)

    def user_guih_01(self):
        '''
        使用人资产归还---待归还界面添加数据
        '''
        self.user_suoyzc_dengz()
        self.user_shouy.apply_business("申请归还")

    def user_guih_02(self):
        '''
        使用人资产归还---归还中界面添加数据
        '''
        self.user_guih_01()
        self.user_guih.guih_pass()

    def user_guih_03(self):
        '''
        使用人资产归还--归还完成界面添加数据
        '''
        self.user_guih_02()
        self.dep_shouy.receipt()

    def user_zhuany_01(self):
        '''
        使用人资产转移--待转移界面添加数据
        '''
        self.user_suoyzc_wdengz()
        self.user_shouy.apply_business("申请转移")

    def user_zhuany_02(self):
        '''
        使用人资产转移--转移中界面添加数据
        '''
        self.user_zhuany_01()
        self.user_zhuany.zhuany("部门")

    def user_zhuany_03(self):
        '''
        使用人资产转移--转移完成界面添加数据
        '''
        self.user_zhuany_02()
        self.dep_shouy.receipt()

    def user_chuz_01(self):
        '''
        使用人我要处置--待提交界面添加数据
        '''
        self.user_suoyzc_dengz()
        self.user_shouy.apply_business("申请处置")

    def user_chuz_02(self):
        '''
        使用人我要处置--审核中界面添加数据
        '''
        self.user_chuz_01()
        self.user_chuz.chuz_ss("提交申请")

    def user_chuz_03(self):
        '''
        使用人我要处置--已审核界面添加数据
        '''
        self.user_chuz_02()
        self.dep_ziccz.chuz_ss("同意")

    def user_yans_01(self):
        '''
        使用人我要处置--已审核界面添加数据
        '''
        self.dep_yans.add_card(card_value="pc服务器")
        self.dep_yans.start_acceptance("添加验收人")

    def user_yans_02(self):
        '''
        使用人我要处置--已审核界面添加数据
        '''
        self.user_yans_01()
        self.user_yans.yans_tj()

    def dep_suoyzc_wdengz(self):
        '''
        部门资产管理员所有资产界面添加未登账卡片
        '''
        self.dep_yans.add_card(card_value="pc服务器")

    def dep_suoyzc_dengz(self):
        '''
        部门资产管理员所有资产界面添加登账卡片
        '''
        self.unit_suoyzc_dengz()
        self.handle.refresh_f5()
        self.unit_fenp.fenp("部门")
        self.dep_shouy.receipt()

    def dep_peiz_01(self):
        '''
        部门资产管理员配置管理--待审核页面添加数据
        '''
        self.user_shenl_03()

    def dep_peiz_02(self):
        '''
        部门资产管理员配置管理--审核中页面添加数据
        '''
        self.dep_peiz_01()
        self.dep_peiz.peiz_ss("送审")

    def dep_peiz_03(self):
        '''
        部门资产管理员配置管理--已审核页面添加数据
        '''
        self.dep_peiz_02()
        self.unit_peiz.peiz_ss("同意")

    def dep_yans_01(self):
        '''
        部门资产管理员验收资产--待验收页面添加数据
        '''
        self.dep_yans.add_card(card_value="pc服务器")

    def dep_yans_02(self):
        '''
        部门资产管理员验收资产--验收中页面添加数据
        '''
        self.dep_yans_01()
        self.dep_yans.start_acceptance()

    def dep_yans_03(self):
        '''
        部门资产管理员验收资产--验收完成页面添加数据
        '''
        self.dep_yans_02()
        self.dep_yans.yansgl_pass()

    def dep_fenp_01(self, value="未登账"):
        '''
        部门资产管理员资产分配--待分配页面添加数据
        value: 登账，未登账
        '''
        if value == "登账":
            self.dep_suoyzc_dengz()
        else:
            self.dep_suoyzc_wdengz()

    def dep_fenp_02(self):
        '''
        部门资产管理员资产分配--分配中页面添加数据
        '''
        self.dep_fenp_01()
        self.handle.refresh_f5()
        self.dep_fenp.fenp("使用人")

    def dep_fenp_03(self):
        '''
        部门资产管理员资产分配--分配完成页面添加数据
        '''
        self.dep_fenp_02()
        self.user_shouy.receipt()

    def dep_guih_01(self):
        '''
        部门资产管理员资产归还--待归还页面添加数据
        '''
        self.unit_fenp_03()

    def dep_guih_02(self):
        '''
        部门资产管理员资产归还--归还中页面添加数据
        '''
        self.dep_guih_01()
        self.dep_guih.guih_pass()

    def dep_guih_03(self):
        '''
        部门资产管理员资产归还--归还完成页面添加数据
        '''
        self.dep_guih_02()
        self.unit_shouy.receipt()

    def dep_shouh_01(self):
        '''
        部门资产管理员资产收回--待收回页面添加数据
        '''
        self.dep_fenp_03()

    def dep_shouh_02(self):
        '''
        部门资产管理员资产收回--收回完成页面添加数据
        '''
        self.dep_shouh_01()
        self.dep_shouh.take_back()

    def dep_zhuany_01(self):
        '''
        部门资产管理员资产转移--待转移页面添加数据
        '''
        self.dep_suoyzc_wdengz()
        self.dep_shouy.apply_business("申请转移")

    def dep_zhuany_02(self):
        '''
        部门资产管理员资产转移--转移中页面添加数据
        '''
        self.dep_zhuany_01()
        self.dep_zhuany.zhuany("使用人")

    def dep_zhuany_03(self):
        '''
        部门资产管理员资产转移--转移完成页面添加数据
        '''
        self.dep_zhuany_02()
        self.user_shouy.receipt()

    def dep_weix_01(self):
        '''
        部门资产管理员维修管理--待审核页面添加数据
        '''
        self.dep_suoyzc_dengz()
        self.dep_shouy.apply_business("申请报修")

    def dep_weix_02(self):
        '''
        部门资产管理员维修管理--审核中页面添加数据
        '''
        self.dep_weix_01()
        self.handle.refresh_f5()
        self.dep_weix.weix_ss("送审")

    def dep_weix_03(self):
        '''
        部门资产管理员维修管理--已审核页面添加数据
        '''
        self.dep_weix_01()
        self.handle.refresh_f5()
        self.dep_weix.weix_ss("同意")

    def dep_weix_04(self):
        '''
        部门资产管理员维修管理--维修完成页面添加数据
        '''
        self.dep_weix_03()
        self.handle.refresh_f5()
        self.dep_weix.weix_yans(1000)

    def dep_chuz_01(self):
        '''
        部门资产管理员资产处置--待审核页面添加数据
        '''
        self.dep_suoyzc_dengz()
        self.dep_shouy.apply_business("申请处置")

    def dep_chuz_02(self):
        '''
        部门资产管理员资产处置--审核中页面添加数据
        '''
        self.dep_chuz_01()
        self.handle.refresh_f5()
        self.dep_ziccz.chuz_ss("送审")

    def dep_chuz_03(self):
        '''
        部门资产管理员资产处置--已审核页面添加数据
        '''
        self.dep_chuz_02()
        self.unit_chuz.chuz_shengcczd()
        self.unit_chuz.chuz_songs()

    def fin_suoyzc_wdengz(self):
        '''
        财务制单人员所有资产界面新增未登账卡片
        '''
        self.unit_suoyzc_wdengz()

    def fin_suoyzc_dengz(self):
        '''
        财务制单人员所有资产界面新增登账卡片
        '''
        self.unit_suoyzc_dengz()

    def fin_xinz_01(self):
        '''
        财务制单人员新增资产--待登账
        '''
        self.unit_dengz_02()

    def fin_xinz_02(self):
        '''
        财务制单人员新增资产--已登账
        '''
        self.unit_dengz_03()

    def fin_hex_01(self):
        '''
        财务制单人员核销资产--待登账
        '''
        self.unit_chuz_03()

    def fin_hex_02(self):
        '''
        财务制单人员核销资产--已登账
        '''
        self.fin_hex_01()
        self.fin_hex.hex_dengz()

    def fin_weix_01(self):
        '''
        财务制单人员资产维修--待登账
        '''
        self.unit_weix_03()

    def fin_weix_02(self, value):
        '''
        财务制单人员资产维修--已登账
        维修费用化登账 value:资本化 or 费用化
        '''
        self.fin_weix_01()
        self.fin_weix.weix_dengz(value)

    def fin_shouyi_01(self, value):
        '''
        财务制单人员收益管理--待登账
        value:处置、出租
        '''
        if value == "处置":
            self.unit_chuz_05()
        elif value == "出租":
            self.unit_chuzu_05()
            self.unit_chuzu.chuzu_shouyi("送财务部门")

    def fin_shouyi_02(self, value):
        '''
        财务制单人员收益管理--已登账
        value:处置、出租
        '''
        self.fin_shouyi_01(value)
        if value == "处置":
            self.fin_hex.hex_dengz()  # 处置先核销
        self.fin_shouy.shouy_dengz()

    def make_init_card(self):
        # 未登帐，更正中、维修中、转移中、分配中、处置中、租借中、投资中、承租借卡片
        self.unit_suoyzc_wdengz()
        self.unit_weix_01()
        self.unit.dep_zhuany_01()
        self.unit_fenp_01()
        self.unit_chuz_01()
        self.unit_chuzu_01()
        self.unit_chengzu_01()


if __name__ == "__main__":
    driver = webdriver.Chrome()
    a = make_date(driver)
    driver.get('http://58.246.240.154:7878/zl/179333')
    driver.maximize_window()
    a.handle.send_value('登录', "username", "ss")
    a.handle.send_value('登录', "password", "123")
    time.sleep(1)
    a.handle.click_element('登录', 'login')
    time.sleep(1)
    n = 1
    sum = 0
    counter = 1
    while counter <= n:
        sum = sum + counter
        counter += 1
        a.unit_chuz_02()
        a.handle.refresh_f5()
