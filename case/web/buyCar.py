# coding=utf-8
from selenium import webdriver
import unittest
import os
import time
from public.login import Mylogin

class Gouwuche(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://101.133.169.100/yuns/index.php")
        self.driver.maximize_window()
        time.sleep(5)

    def tearDown(self):
        filedir = "C:/test/screenshot/"
        if not os.path.exists(filedir):
            os.makedirs(os.path.join('C:/', 'test', 'screenshot'))
        screen_name = filedir + time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time())) + ".png"
        self.driver.get_screenshot_as_file(screen_name)
        self.driver.quit()


    def testGouwu01_03(self):
        '''购物车为空时文案显示是否正常'''
        Mylogin(self.driver).login()
        self.driver.find_element_by_xpath("//div[@class='small_cart_name']/span").click()
        time.sleep(3)
        emptyGouwuText = self.driver.find_element_by_xpath("//div[@class='r']/span")
        print(emptyGouwuText.text)
        self.assertEqual("购物车内暂时没有商品",emptyGouwuText.text)



if __name__ == "__main__":
    unittest.main()


