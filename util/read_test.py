#encoding: utf-8

import sys
import os
import time
sys.path.append(os.path.join(os.getcwd()))
from selenium import webdriver
driver = webdriver.Chrome()
driver.get('http://58.246.240.154:7878/zl/6666')
time.sleep(5)
'''
class Librarytest:
    def libimport(self):
        print('Library keywords import')
'''


#回调keyword方法
def call_method(method, *args):
    try:
        method(*args)
        return method(*args)
    except:
        pass


#导入-解析-执行
def robotexc(key):
    #类名
    clsname = "YansglPage"
    #方法名
    funname = "add_card"

    #导入模块名，即库文件名称
    obj = __import__("page.Unit.yansgl_page", fromlist=True)
    #获取类对象
    cls = getattr(obj, clsname)
    #新建类对象
    newobj = cls(driver)
    #获取方法，即keyword
    fun = getattr(newobj, funname)
    #调用方法
    call_method(fun)


robotexc()