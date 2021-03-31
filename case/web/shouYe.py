# coding=utf-8
from selenium import webdriver
from public.login import Mylogin
import unittest
import os
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from public import mkstr

class TestShouye(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://101.133.169.100:8088/index.html")
        self.driver.maximize_window()
        time.sleep(5)
        print("starttime:" + time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time())))

    def tearDown(self):
        filedir = "C:/test/screenshot/"
        if not os.path.exists(filedir):
            os.makedirs(os.path.join('C:/', 'test', 'screenshot'))
        print("endTime:" + time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time())))
        screen_name = filedir + time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time())) + ".png"
        self.driver.get_screenshot_as_file(screen_name)
        self.driver.quit()


    def testShouye001(self):
        '''验证首页右上角用户信息显示是否正常'''
        Mylogin(self.driver).login()
        #右上角名称控件
        loginText = self.driver.find_element_by_xpath("//*[@id='app']/section/header/div/span[2]/div[2]/div/div/div/div")
        #名称左边控件
        regisText = self.driver.find_element_by_xpath("//*[@id='app']/section/header/div/span[1]/button")

        self.assertEqual("吴广",loginText.text)
        self.assertEqual("开通授权", regisText.text)
        # self.assertEqual("退出", regisText.text)
        # self.assertNotEqual("dd", regisText.text)
        #
        # self.assertIn("云商系统商城",firstPageNavi.text)#后者包含前者
        #
        # self.assertTrue(self.driver.find_element_by_xpath("//div[@class='top']/span").is_displayed())
        # self.assertFalse(firstPageNavi.is_displayed())
        #
        # if loginText.text == "177****0979":
        #     print("等于")
        # else:
        #     print("不等于")
        #     self.driver.find_element_by_xpath("王麻子")

    def testShouye002(self):
        '''验证查看登录页面展示是否正常'''
        Mylogin(self.driver).login()
        #办公控件
        workText = self.driver.find_element_by_xpath('//*[@id="app"]/section/header/div/div/div/a[1]/div')
        #客户管理控件
        crmText = self.driver.find_element_by_xpath('//*[@id="app"]/section/header/div/div/div/a[2]/div')
        #商业智能控件
        biText = self.driver.find_element_by_xpath('//*[@id="app"]/section/header/div/div/div/a[3]/div')
        #项目管理控件
        projectText = self.driver.find_element_by_xpath('//*[@id="app"]/section/header/div/div/div/a[4]/div')
        #办公样式控件
        workClass = self.driver.find_element_by_xpath('//*[@id="app"]/section/header/div/div/div/a[1]')

        self.assertEqual("办公",workText.text)
        self.assertEqual("客户管理", crmText.text)
        self.assertEqual("商业智能", biText.text)
        self.assertEqual("项目管理", projectText.text)
        self.assertIn("router-link-active",workClass.get_attribute('class'))#判断默认页面是否为办公页面


if __name__ == "__main__":
    unittest.main()


