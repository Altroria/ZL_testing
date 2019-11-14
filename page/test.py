#coding=utf-8
'''
登录业务层
'''
import sys
import os
sys.path.append(os.path.join(os.getcwd()))
from selenium import webdriver
import time
from config import url
from base.base_handle import BaseHandle

driver = webdriver.Chrome()
driver.get('https://www.humanbenchmark.com/tests/reactiontime')


driver.find_element_by_xpath('//*[@id="root"]/div/div[4]/div[1]/div/div[1]/div[2]/div[1]/h1')
time.sleep(5)
print("开始")
driver.find_element_by_xpath('//*[@id="root"]/div/div[4]/div[1]/div/div[1]/h1/i')
print("准备")
time.sleep(5)
driver.find_element_by_xpath('//*[@id="root"]/div/div[4]/div[1]/div/div[1]/h1/div')


time.sleep(10)
