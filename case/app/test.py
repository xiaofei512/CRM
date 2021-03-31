import os
import unittest
import time
from appium import webdriver


class AndroidTests(unittest.TestCase):
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '7.1.2'
        desired_caps['deviceName'] = 'Android Emulator'
        desired_caps['noReset'] = 'True'
        desired_caps['appPackage'] = 'cn.xiaochuankeji.tieba'
        desired_caps['appActivity'] = '.ui.base.SplashActivity'

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def tearDown(self):
        self.driver.quit()
        pass

    def test_elements_by_id001(self):
        self.driver.implicitly_wait(60)
        time.sleep(10)
        el = self.driver.find_elements_by_id("cn.xiaochuankeji.tieba:id/title")
        print(el.text)
        el.click()
        self.driver.implicitly_wait(10)
        #定位第二个昵称
        el2 = self.driver.find_elements_by_id("cn.xiaochuankeji.tieba:id/simple_member_tv_name")
        print(el2[1].text)
        el2[1].click()

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(AndroidTests)
    unittest.TextTestRunner(verbosity=2).run(suite)