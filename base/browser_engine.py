#coding=utf-8
"""
  @desc: 浏览器引擎
"""
import os

from selenium import webdriver

from config import settings


class BrowserEngine(object):
    CURRENT_PATH = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), '../resource')
    CHROME_DRIVER = os.path.join(CURRENT_PATH, 'chromedriver.exe')
    FIREFOX_DRIVER = os.path.join(CURRENT_PATH, 'geckodriver.exe')
    IE_DRIVER = os.path.join(CURRENT_PATH, 'IEDriverServer.exe')

    def __init__(self, browser=None):
        if browser is None:
            self._browser_type = settings.DEFAULT_BROWSER
        else:
            self._browser_type = browser
        self._driver = None

    #初始化driver
    def init_driver(self):
        if self._browser_type.lower() == 'chrome':
            option = webdriver.ChromeOptions()
            #option.add_argument('--headless')  # 后台执行
            #option.add_argument('--no-sandbox')  # 取消沙盒模式
            #option.add_argument('--start-maximized')  # 启动就最大化
            self._driver = webdriver.Chrome(
                executable_path=self.CHROME_DRIVER, options=option)
        elif self._browser_type.lower() == 'firefox':
            self._driver = webdriver.Firefox(
                executable_path=self.FIREFOX_DRIVER)
        elif self._browser_type.lower() == 'ie':
            self._driver = webdriver.Ie(executable_path=self.IE_DRIVER)
        else:
            ValueError('传入的浏览器类型错误,目前仅支持Chrome/Firefox/IE.')
        self._driver.implicitly_wait(
            time_to_wait=settings.UI_WAIT_TIME)  # 隐式等待
        return self._driver
