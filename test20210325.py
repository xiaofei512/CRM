# coding=utf-8
from selenium import webdriver
from public.login import Mylogin
import unittest
import os
import time
from public import mkstr

driver = webdriver.Chrome()
driver.get("http://101.133.169.100:8088/index.html")
driver.maximize_window()
time.sleep(5)
print("starttime:" + time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time())))

driver.find_element_by_name("username").send_keys("18621796828")
driver.find_element_by_name("password").send_keys("123456")
driver.find_element_by_xpath("//button[@type='button']").click()
time.sleep(5)