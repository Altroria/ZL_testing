#coding = utf-8
import os
import sys
import time
import cx_Oracle
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))
from pykeyboard import PyKeyboard
from util.read_init import ReadIni
from util.handle_json import handle_json
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


class SeleniumDriver(object):
    def __init__(self, driver):
        self.driver = driver

    def get_url(self, url):
        if self.driver != None:
            time.sleep(1)
            self.driver.maximize_window()
            if 'http' in url:
                self.driver.get(url)
            elif 'D' in url:
                self.driver.get(url)
            else:
                print("你的URL有问题")
        else:
            print("case失败")

    def handle_windows(self, *args):
        value = len(args)
        if value == 1:
            if args[0] == 'max':
                self.driver.maximize_window()
            elif args[0] == 'min':
                self.driver.minimize_window()
            elif args[0] == 'back':
                self.driver.back()
            elif args[0] == 'go':
                self.driver.forward()
            else:
                self.driver.refresh()
        elif value == 2:
            self.driver.set_window_size(args[0], args[1])
        else:
            print("你传递的参数有问题")

    def assert_title(self, title_name=None):
        '''
        判断title是否正确
        '''
        if title_name != None:
            get_title = EC.title_contains(title_name)
            return get_title(self.driver)

    def open_url_is_true(self, url, title_name=None):
        '''
        通过title判断页面是否正确

        '''
        self.get_url(url)
        return self.assert_title(title_name)

    def close_driver(self):
        self.driver.close()

    def switch_windows(self, title_name=None):
        '''
        切换windows
        '''
        handl_list = self.driver.window_handles
        current_handle = self.driver.current_window_handle
        for i in handl_list:
            if i != current_handle:
                time.sleep(1)
                self.driver.switch_to.window(i)
                if self.assert_title(title_name):
                    break

    def element_isdisplay(self, element):
        flag = element.is_displayed()
        if flag == True:
            return element
        else:
            return False

    def is_element_visible(self, by, info, index=None):
        if index == None:
            element = self.get_element(by, info)
        else:
            element = self.get_list_element(by, info, index)
        flag = element.is_displayed()
        if flag == True:
            return True
        else:
            return False

    #等待元素显示
    def wait_element(self, by, info):
        by, value = self.get_local_element(by, info)
        if by == 'id':
            locator = (By.ID, value)
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(locator))
        elif by == 'name':
            locator = (By.NAME, value)
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(locator))
        elif by == 'css':
            locator = (By.CSS_SELECTOR, value)
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(locator))
        elif by == 'class':
            locator = (By.CLASS_NAME, value)
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(locator))
        elif by == 'link_text':
            locator = (By.LINK_TEXT, value)
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(locator))
        elif by == 'xpath':
            locator = (By.XPATH, value)
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(locator))

    #等待元素消失
    def wait_element_not(self, by, info):
        by, value = self.get_local_element(by, info)
        if by == 'id':
            locator = (By.ID, value)
            WebDriverWait(self.driver, 5).until_not(
                EC.visibility_of_element_located(locator))
        elif by == 'name':
            locator = (By.NAME, value)
            WebDriverWait(self.driver, 5).until_not(
                EC.visibility_of_element_located(locator))
        elif by == 'css':
            locator = (By.CSS_SELECTOR, value)
            WebDriverWait(self.driver, 5).until_not(
                EC.visibility_of_element_located(locator))
        elif by == 'class':
            locator = (By.CLASS_NAME, value)
            WebDriverWait(self.driver, 5).until_not(
                EC.visibility_of_element_located(locator))
        elif by == 'link_text':
            locator = (By.LINK_TEXT, value)
            WebDriverWait(self.driver, 5).until_not(
                EC.visibility_of_element_located(locator))
        elif by == 'xpath':
            locator = (By.XPATH, value)
            WebDriverWait(self.driver, 5).until_not(
                EC.visibility_of_element_located(locator))

    def get_element(self, by, info):
        '''
        获取元素element
        @parame by 定位方式
        @parame value 定位置
        @return element 返回一个元素
        '''
        by, value = self.get_local_element(by, info)
        element = None
        try:
            if by == 'id':
                element = self.driver.find_element_by_id(value)
            elif by == 'name':
                element = self.driver.find_element_by_name(value)
            elif by == 'css':
                element = self.driver.find_element_by_css_selector(value)
            elif by == 'class':
                element = self.driver.find_element_by_class_name(value)
            elif by == 'link_text':
                element = self.driver.find_element_by_link_text(value)
            elif by == 'xpath':
                element = self.driver.find_element_by_xpath(value)
            else:
                element = self.driver.find_element_by_tag_name(value)
            return element
        except:
            return None

    def get_elements(self, by, info):
        '''
        获取元素elements
        @parame by 定位方式
        @parame value 定位置
        @return elements 返回一个元素
        '''
        elements = None
        element_list = []
        by, value = self.get_local_element(by, info)
        try:
            if by == 'id':
                elements = self.driver.find_elements_by_id(value)
            elif by == 'name':
                elements = self.driver.find_elements_by_name(value)
            elif by == 'css':
                elements = self.driver.find_elements_by_css_selector(value)
            elif by == 'class':
                elements = self.driver.find_elements_by_class_name(value)
            else:
                elements = self.driver.find_elements_by_xpath(value)

            for element in elements:
                if self.element_isdisplay(element) == False:
                    continue
                else:
                    element_list.append(element)
            return element_list
        except:
            return None

    def get_level_element(self,
                          by,
                          info_level,
                          node_bys,
                          node_info,
                          index=None):
        '''
        层级定位
        有一个父节点
        父节点找子节点
        '''
        element = self.get_element(by, info_level)
        node_by, node_value = self.get_local_element(node_bys, node_info)
        if element == False:
            return False

        node_element = None
        element_list = []
        try:
            if node_by == 'id':
                node_element = element.find_elements_by_id(node_value)
            elif node_by == 'name':
                node_element = element.find_elements_by_name(node_value)
            elif node_by == 'css':
                node_element = element.find_elements_by_css_selector(
                    node_value)
            elif node_by == 'class':
                node_element = element.find_elements_by_class_name(node_value)
            else:
                node_element = element.find_elements_by_xpath(node_value)
        except:
            return None
        for element_new in node_element:
            if self.element_isdisplay(element_new) == False:
                continue
            else:
                element_list.append(element_new)
        return element_list[index]

    def get_list_element(self, by, info, index):
        '''
        通过list定位我们得元素
        #2
        #1
        '''
        elements = self.get_elements(by, info)
        if index > len(elements):
            return None
        return elements[index]

    def send_value(self, by, info, key=None, index=None):
        '''
        输入值
        '''
        if key != None:
            if index == None:
                element = self.get_element(by, info)
            else:
                element = self.get_list_element(by, info, index)

            if element == False:
                print("输入失败，定位没有展现出来。")
            else:
                if element != None:
                    element.clear()
                    element.send_keys(key)
                else:
                    print("输入失败，定位元素没找到。")
        else:
            return None

    def clear_input(self, by, info, index=None):
        '''
        清空输入框
        '''
        if index == None:
            element = self.get_element(by, info)
        else:
            element = self.get_list_element(by, info, index)

        if element == False:
            print("输入失败，定位没有展现出来。")
        else:
            if element != None:
                element.clear()
            else:
                print("输入失败，定位元素没找到。")

    def click_element(self, by, info, index=None):
        '''
        点击元素
        '''
        if index == None:
            element = self.get_element(by, info)
        else:
            element = self.get_list_element(by, info, index)
        element.click()

    def right_click(self, by, info, index=None):
        '''
        右键点击元素
        '''
        if index == None:
            element = self.get_element(by, info)
        else:
            element = self.get_list_element(by, info, index)
        if element != False:
            if element != None:
                ActionChains(self.driver).context_click(element).perform()
            else:
                print("点击失败，定位元素没找到")
        else:
            print("点击失败，元素不可见")

    def check_box_isselected(self, by, info, check=None):
        '''
        判断元素是否选中
        如果没选中就选中，如果选中就补选中，根据参数来
        '''
        element = self.get_element(by, info)
        if element != "False":
            flag = element.is_selected()
            if flag == True:
                if check != 'check':
                    self.click_element(info)
            else:
                if check == 'check':
                    self.click_element(info)
        else:
            print("元素不可见，没办法选中")

    def get_local_element(self, by, info):
        read_ini = ReadIni()
        '''
        读取ini配置文件
        '''
        data = read_ini.get_value(by, info)
        data_info = data.split('>')
        return data_info

    def get_menu_value(self, by, value):
        read_menu = ReadIni("menu.ini")
        '''
        读取menu_ini配置文件
        '''
        data = read_menu.get_value(by, value)
        data_info = data.split('>')
        return data_info

    def get_class_value(self, by, value):
        read_menu = ReadIni("class.ini")
        '''
        读取class_ini配置文件
        '''
        data = read_menu.get_value(by, value)
        data_info = data.split('>')
        return data_info

    def get_selected(self, by, info, value_index, index=None):
        '''
        通过index获取我们selected，然后选择我们selected
        '''
        selected_element = None
        if index != None:
            selected_element = self.get_list_element(by, info, index)
        else:
            selected_element = self.get_element(by, info)
        Select(selected_element).select_by_index(value_index)

    def upload_file(self, file_name):
        '''
        非input类型上传文件
        @parame filename
        '''
        pykey = PyKeyboard()
        #pykey.tap_key(pykey.shift_key)
        pykey.type_string(file_name)
        time.sleep(2)
        pykey.tap_key(pykey.enter_key)

    def download_file(self, info):
        '''
        下载文件
        '''
        self.click_element(info)

    def js_excute_calendar(self, by, info, index=None):
        '''
        执行js
        '''
        local = self.get_local_element(by, info)
        by = local[0]
        value = local[1]
        if by == 'id':
            by_key = 'getElementById'
            js = 'document.%s("%s").removeAttribute("readonly");' % (by_key,
                                                                     value)
        else:
            by_key = 'getElementsByClassName'
            js = 'document.%s("%s")[%s].removeAttribute("readonly");' % (
                by_key, value, index)
        self.driver.execute_script(js)

    def caledar(self, by, info, value, index=None):
        '''
        修改日历
        '''
        if index != None:
            element = self.get_list_element(by, info, index)
            try:
                element.get_attribute('readonly')
                self.js_excute_calendar(by, info, index)
            except:
                print("这个不是只读属性的日历")
            element.clear()
            self.send_value(by, info, value, index)
        else:
            element = self.get_element(by, info)
            try:
                element.get_attribute('readonly')
                self.js_excute_calendar(by, info)
            except:
                print("这个不是只读属性的日历")
            element.clear()
            self.send_value(by, info, value)

    def moveto_element_mouse(self, by, info):
        '''
        移动鼠标到某个元素上
        '''
        element = self.get_element(by, info)
        ActionChains(self.driver).move_to_element(element).perform()

    def refresh_f5(self):
        '''
        强制刷新
        '''
        #ActionChains(self.driver).key_down(Keys.CONTROL).send_keys(Keys.F5).key_up(Keys.CONTROL).perform()
        self.driver.refresh()

    def switch_iframe(self, by=None, info=None):
        '''
        切换iframe
        '''
        if info != None:
            iframe_element = self.get_element(by, info)
            if iframe_element == None:
                print("iframe错误")
            else:
                self.driver.switch_to.frame(iframe_element)
        else:
            self.driver.switch_to.default_content()

    def switch_alert(self, info, value=None):
        '''
        系统级弹窗
        @parame info 确认or取消
        @parame value 是否需要输入的值
        '''
        windows_alert = self.driver.switch_to.alert
        if info == 'accept':
            if value == None:
                windows_alert.accept()
            else:
                windows_alert.send_keys(value)
                windows_alert.accept()
        else:
            windows_alert.dismiss()

    def scroll_get_element(self, list_info, str_info):
        '''
        通过滚动条 ，滚动查找元素
        '''
        t = True
        list_element = self.get_elements(list_info)
        js = 'document.documentElement.scrollTop=100000;'
        while t:
            for element in list_element:
                title_name = element.find_element_by_tag_name('p').text
                if title_name in str_info:
                    element.click()
                    t = False
            self.driver.execute_script(js)
            time.sleep(3)

    def scroll_element(self, info):
        js = 'document.documentElement.scrollTop=100000;'
        t = True
        while t:
            try:
                self.get_element(info)
                t = False
            except:
                self.driver.execute_script(js)
                time.sleep(3)

    def get_cookie(self):
        #接口
        #依赖
        cookie = self.driver.get_cookies()
        handle_json.write_data(cookie)

    def set_cookie(self):
        '''
        植入cookie
        '''
        cookie = handle_json.get_data()
        self.driver.delete_all_cookies()
        time.sleep(1)
        self.driver.add_cookie(cookie)
        time.sleep(2)

    def save_png(self):
        '''
        截取当前界面
        '''
        now_time = time.strftime("%Y%m%d.%H.%M.%S")
        self.driver.get_screenshot_as_file('%s.png' % now_time)

    def sleep_time(self):
        '''
        等待
        '''
        time.sleep(2)

    def close_brower(self):
        '''
        关闭浏览器
        '''
        self.driver.close()

    #----------------->数据库操作<----------------
    def get_database_value(self, by, value):
        read_database = ReadIni("DataBase.ini")
        '''
        读取database_ini配置文件
        '''
        data = read_database.get_value(by, value)
        data_info = data.split('>')
        return data_info

    #获取数据库数据
    def get_database_data(self, sql):
        address = 'zx/zl123456zl@164_XE'
        self.conn = cx_Oracle.connect(address)
        self.curs = self.conn.cursor()
        self.curs.execute(sql)
        row = self.curs.fetchone()
        return row
        self.close_database()

    #获取数据库行数
    def get_database_lines(self, value):
        surface, state = self.get_database_value("单位资产管理员", value)
        Unit_ID = self.get_database_value("单位资产管理员", "单位id")[1]
        sql = 'select count(*) FROM %s where orgid=%s and %s' % (
            surface, Unit_ID, state)
        rows = self.get_database_data(sql)
        for i in rows:
            return i
        self.close_database()

    #获取所有资产，未在业务中的卡片编号
    def get_card_number(self, value=None):
        Unit_ID = self.get_database_value("单位资产管理员", "单位id")[1]
        if value == '使用人':
            sql = "select * from (select objcode from bs_ast_card where orgid=%s and caiwrzrq is not null and yewid is null and shiybmid is not null and shiyrid is not null) where rownum=1" % (
                Unit_ID)
        elif value == '部门资产管理员':
            sql = "select * from (select objcode from bs_ast_card where orgid=%s and caiwrzrq is not null and yewid is null and shiybmid is not null) where rownum=1" % (
                Unit_ID)
        else:
            sql = "select * from (select objcode from bs_ast_card where orgid=%s and caiwrzrq is not null and yewid is null ) where rownum=1" % (
                Unit_ID)
        try:
            rows = self.get_database_data(sql)
            for i in rows:
                return i
        except:
            return None
        self.close_database()

    #获取开关"是否启用权限管理"的状态
    def get_switch(self, value):
        Unit_ID = self.get_database_value("单位资产管理员", "单位id")[1]
        sql = "select a.v from core_sysoptmx a left join core_sysopt b on a.sysoptid = b.rwid where a.orgid =%s and b.title = '是否启用权限管理'" % (
            Unit_ID)
        rows = self.get_database_data(sql)
        for i in rows:
            return i
        self.close_database()

    #关闭数据库
    def close_database(self):
        self.curs.close()
        self.conn.close()
