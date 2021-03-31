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
        #self.driver.quit()
        pass

    def test_element_by_id(self):
        self.driver.implicitly_wait(60)
        el = self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/title")
        print(el.text)
        el.click()

    def test_element_by_id001(self):
        #定位话题
        self.driver.implicitly_wait(60)
        el = self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/topic")
        print(el.text)
        el.click()

    def test_element_by_id002(self):
        #定位搜索
        self.driver.implicitly_wait(60)
        el = self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/search_b")
        print(el.text)
        el.click()


    def test_element_by_id003(self):
        #定位昵称
        self.driver.implicitly_wait(60)
        el = self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/simple_member_tv_name")
        print(el.text)
        el.click()

    def test_element_by_id004(self):
        #定位我的
        self.driver.implicitly_wait(60)
        el = self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/me_item")
        print(el.text)
        el.click()

    def test_element_by_id005(self):
        #定位头像
        self.driver.implicitly_wait(60)
        el = self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/avatar_view_strokec")
        print(el.text)
        el.click()

    def test_elements_by_id001(self):
        self.driver.implicitly_wait(60)
        el = self.driver.find_elements_by_id("cn.xiaochuankeji.tieba:id/title")
        print(el.text)
        el.click()
        self.driver.implicitly_wait(5)
        #定位第二个昵称
        el2 = self.driver.find_elements_by_id("cn.xiaochuankeji.tieba:id/simple_member_tv_name")
        print(el2[1].text)
        el2[1].click()

    def test_elements_by_id002(self):
        self.driver.implicitly_wait(60)
        el = self.driver.find_elements_by_id("cn.xiaochuankeji.tieba:id/title")
        print(el.text)
        el.click()
        self.driver.implicitly_wait(5)
        #定位第二个认证标签
        el2 = self.driver.find_elements_by_id("cn.xiaochuankeji.tieba:id/simple_member_tv_description")
        print(el2[1].text)
        el2[1].click()

    def test_elements_by_id003(self):
        self.driver.implicitly_wait(60)
        el = self.driver.find_elements_by_id("cn.xiaochuankeji.tieba:id/title")
        print(el[3].text)
        el[3].click()
        self.driver.implicitly_wait(5)
        #定位第二个图片
        el2 = self.driver.find_elements_by_id("cn.xiaochuankeji.tieba:id/holder_flow_rmdv")
        print(el2[1].size)
        el2[1][1].click()

    def test_elements_by_id004(self):
        self.driver.implicitly_wait(60)
        el = self.driver.find_elements_by_id("cn.xiaochuankeji.tieba:id/textTabItem")
        #定位到动态
        print(el[1].text)
        el[1].click()


    def test_elements_by_id005(self):
        self.driver.implicitly_wait(60)
        el = self.driver.find_elements_by_id("cn.xiaochuankeji.tieba:id/iconTabItem")
        #定位到消息的图标
        print(el[3].text)
        el[3].click()



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(AndroidTests)
    unittest.TextTestRunner(verbosity=2).run(suite)