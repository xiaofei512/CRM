import os
import unittest
import time
from public.loginApp import Mylogin
from appium import webdriver

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class AndroidTests(unittest.TestCase):
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '5.1'
        desired_caps['deviceName'] = 'Android Emulator'
        desired_caps['noReset'] = 'True'
        desired_caps['app'] = PATH('E:/newCourse/zuiyou518.apk')
        desired_caps['unicodeKeyboard'] = 'True'
        desired_caps['resetKeyboard'] = 'True'
        desired_caps['appPackage'] = 'cn.xiaochuankeji.tieba'
        desired_caps['appActivity'] = '.ui.base.SplashActivity'

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def tearDown(self):
        self.driver.quit()

    def testshouye01_01(self):
        '''验证首页导航栏文案显示是否正常'''
        time.sleep(8)
        self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/home_item").click()
        time.sleep(6)
        navText = self.driver.find_elements_by_id("cn.xiaochuankeji.tieba:id/title")
        self.assertEqual(navText[0].text, "关注")
        self.assertEqual(navText[1].text, "推荐")
        self.assertEqual(navText[2].text, "视频")
        self.assertEqual(navText[3].text, "图文")


    def testshouye01_02(self):
        '''验证帖子列表内容跳转'''
        time.sleep(8)
        aa = self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/expand_content_view")
        bb = aa.text
        aa.click()
        time.sleep(3)
        forumDetailText = self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/tvTitle")
        cc = self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/ss")
        self.assertEqual(forumDetailText.text,"帖子详情")
        self.assertEqual(bb,cc.text)


    def testshouye01_03(self):
        '''验证评论帖子功能'''
        Mylogin(self.driver).login()
        time.sleep(3)
        self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/iconTabItem").click()
        time.sleep(6)
        self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/expand_content_view").click()
        time.sleep(3)
        self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/etInput").send_keys("textCESHI")
        self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/send").click()
        sendContent = self.driver.find_elements_by_id("cn.xiaochuankeji.tieba:id/expandTextView")
        sendContentRawList = []
        for i in range(0, len(sendContent)):
            sendContentRawList.append(sendContent[i].text)
        sendContentList = "".join(sendContentRawList)
        self.assertIn("textCESHI", sendContentList)


if __name__ == "__main__":
    unittest.main()