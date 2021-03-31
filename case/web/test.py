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
from selenium.webdriver.common.keys import Keys
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

    def testLog021(self):
        '''验证删除回复日志内容和提示显示'''
        Mylogin(self.driver).login()
        #点击日志
        WebDriverWait(self.driver,20,0.5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/section/section/aside/div/ul/a[5]/li/span')))
        self.driver.find_element_by_xpath('//*[@id="app"]/section/section/aside/div/ul/a[5]/li/span').click()
        WebDriverWait(self.driver, 20, 0.5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="pane-1"]/div[1]/div[2]/div[1]/div[2]/button/span')))
        #点击回复
        self.driver.find_element_by_xpath('//*[@id="pane-1"]/div[1]/div[2]/div[1]/div[2]/button/span').click()
        time.sleep(5)
        reply = "回复时间：" + time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
        #输入回复内容
        self.driver.find_element_by_xpath('//*[@id="pane-1"]/div[1]/div[2]/div[1]/div[3]/div/textarea').send_keys(reply)
        #点击回复提交
        self.driver.find_element_by_xpath('//*[@id="pane-1"]/div[1]/div[2]/div[1]/div[3]/div/textarea/../../div[2]/div/button[1]/span').click()
        WebDriverWait(self.driver, 20, 0.5).until(
            EC.presence_of_element_located((By.XPATH, '//div[@id="pane-1"]/div/div[2]/div[1]/div[1]/div[4]/div[2]/div[2]/span[1]')))
        #点击删除
        self.driver.find_element_by_xpath('//div[@id="pane-1"]/div/div[2]/div[1]/div[1]/div[4]/div[2]/div[2]/span[1]').click()
        time.sleep(10)
        self.driver.implicitly_wait(10)
        #点击确定
        self.driver.find_element_by_xpath('/html/body/div/div/div/button[2]').click()
        WebDriverWait(self.driver, 10, 0.1).until(
            EC.presence_of_element_located((By.XPATH, '//div[@role="alert"]/p')))
        #获取提示内容
        makeText = self.driver.find_element_by_xpath("//div[@role='alert']/p")
        self.assertEqual(makeText.text,'删除成功!')
        try:
            WebDriverWait(self.driver, 20, 0.5).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@id="pane-1"]/div/div[2]/div[1]/div[1]/div[4]/div[2]/div[2]/span[1]')))
            # 点击删除
            self.driver.find_element_by_xpath(
                '//div[@id="pane-1"]/div/div[2]/div[1]/div[1]/div[4]/div[2]/div[2]/span[1]').click()
            time.sleep(10)
            self.driver.implicitly_wait(10)
            # 点击确定
            self.driver.find_element_by_xpath('/html/body/div/div/div/button[2]').click()
        except:
            pass
        time.sleep(3)
        #获取所有回复内容
        sendContent = self.driver.find_elements_by_css_selector('.reply-title>span')
        sendContentRawList = []
        for i in range(0, len(sendContent)):
            sendContentRawList.append(sendContent[i].text)
        sendContentList = "".join(sendContentRawList)
        self.assertNotIn(reply, sendContentList)





    # def testLog012(self):
    #     '''验证快速创建日志，明天工作内容输入1001个字母，提示是否正确'''
    #     Mylogin(self.driver).login()
    #     self.driver.find_element_by_xpath('//*[@id="app"]/section/section/aside/div/ul/a[5]/li').click()
    #     time.sleep(3)
    #     self.driver.find_element_by_xpath('//div[@id="pane-1"]/div/div[1]/div[1]/div/div/span/span/i').click()
    #     time.sleep(2)
    #     ele = self.driver.find_element_by_xpath("//div[@class='form']/div[2]/label")
    #     ActionChains(self.driver).move_to_element(ele).perform()#悬停鼠标位置
    #     time.sleep(3)
    #     self.driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/ul/li[2]/span').click()
    #
    #     # self.assertEqual(makeText.text, "新建失败")#验证提示信息
    #     # self.assertEqual(url1, url2)  #验证返回界面



if __name__ == "__main__":
    unittest.main()
