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

    def testBangong001(self):
        '''验证查看办公页面默认展示是否正常'''
        Mylogin(self.driver).login()
        WebDriverWait(self.driver,20,0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/section/header/div/div/div/a[4]/div')))
        self.driver.find_element_by_xpath('//*[@id="app"]/section/header/div/div/div/a[4]/div').click()#点击项目管理
        WebDriverWait(self.driver,10,0.5).until(EC.presence_of_element_located((By.XPATH, '//span[text()="归档项目"]')))
        self.driver.find_element_by_xpath('//*[@id="app"]/section/header/div/div/div/a[1]/div').click()#点击办公
        WebDriverWait(self.driver,10,0.5).until(EC.presence_of_element_located((By.XPATH, '//span[text()="工作台"]')))
        #工作台样式控件
        workClass = self.driver.find_element_by_xpath('//span[text()="工作台"]/../..')
        self.assertIn("active",workClass.get_attribute('class'))#判断默认页面是否为工作台页面

    def testLog001(self):
        '''验证快速创建日志，不输入直接提交日志，提示语是否正常'''
        Mylogin(self.driver).login()
        Mylogin(self.driver).mklog()
        self.driver.find_element_by_xpath("//div[@class='el-card__body']/div/div/button[1]/span").click()
        warnText = self.driver.find_element_by_xpath("/html/body/div/p")#获取提示信息
        time.sleep(2)
        submit = self.driver.find_element_by_xpath("//div[@class='el-card__body']/div/div/button[1]/span")
        self.assertEqual(warnText.text, "内容至少填写一项")#验证提示信息
        self.assertEqual(submit.text,'提交')#验证页面是否跳转

    def testLog002(self):
        '''验证快速创建日志，直接关闭新建日志页面，返回页面是否是之前的页面'''
        Mylogin(self.driver).login()
        time.sleep(5)
        url1 = self.driver.current_url#获取页面地址信息
        Mylogin(self.driver).mklog()
        #等待关闭按钮显示
        element = WebDriverWait(self.driver, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, "//*[@class='header']/img")))
        element.click()
        #等待页面关闭跳转
        WebDriverWait(self.driver, 10, 0.5).until(
            EC.presence_of_element_located((By.XPATH, "//*[text()='客户管理']")))
        url2 = self.driver.current_url#获取页面地址信息
        self.assertEqual(url1, url2)#验证页面信息是否相同

    def testLog003(self):
        '''验证快速创建日志，默认页面是否为日报'''
        Mylogin(self.driver).login()
        Mylogin(self.driver).mklog()
        dailyReport = self.driver.find_element_by_xpath("//div[@class='el-card__body']/div/div[2]/div[1]/div[1]/div/div/div/div[2]")
        self.assertEqual(dailyReport.get_attribute('aria-selected'), "true")#验证提示信息
        self.assertEqual(dailyReport.text,'日报')

    def testLog004(self):
        '''验证明天工作内容框输入汉字，提示是否正确，返回日志页面'''
        Mylogin(self.driver).login()
        Mylogin(self.driver).mklog()
        self.driver.find_element_by_xpath("//div[@class='form']/div[2]/div/textarea").send_keys('明天工作内容是拜访客服')#输入汉字
        self.driver.find_element_by_xpath("//div[@class='el-card__body']/div/div/button[1]/span").click()
        try:
            self.driver.implicitly_wait(10)
            makeText = self.driver.find_element_by_xpath("//div[@role='alert']/p")
            self.assertEqual(makeText.text,'新建成功')
            print("提示：新建成功")
        except:
            pass
        WebDriverWait(self.driver, 10, 0.5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/section/section/aside/div/ul/a[5]/li/span')))
        journal = self.driver.find_element_by_xpath('//*[@id="app"]/section/section/aside/div/ul/a[5]/li')
        journalText = self.driver.find_element_by_xpath('//*[@id="app"]/section/section/aside/div/ul/a[5]/li/span')
        allof = self.driver.find_element_by_xpath('//div[@id="tab-1"]')
        allofText = self.driver.find_element_by_xpath('//div[@id="tab-1"]/div/span')
        self.assertEqual(journalText.text, '日志')  #验证返回界面
        self.assertIn('menu-item-select',journal.get_attribute('class'))
        self.assertEqual(allofText.text, '全部')  #验证返回全部页面
        self.assertEqual('true',allof.get_attribute('aria-selected'))

    def testLog005(self):
        '''验证明天工作内容框输入数字，提示是否正确，返回日志页面'''
        Mylogin(self.driver).login()
        Mylogin(self.driver).mklog()
        self.driver.find_element_by_xpath("//div[@class='form']/div[2]/div/textarea").send_keys(mkstr.digits(10))#输入数字
        self.driver.find_element_by_xpath("//div[@class='el-card__body']/div/div/button[1]/span").click()
        try:
            self.driver.implicitly_wait(10)
            makeText = self.driver.find_element_by_xpath("//div[@role='alert']/p")
            self.assertEqual(makeText.text,'新建成功')
            print("提示：新建成功")
        except:
            pass
        WebDriverWait(self.driver, 10, 0.5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/section/section/aside/div/ul/a[5]/li/span')))
        journal = self.driver.find_element_by_xpath('//*[@id="app"]/section/section/aside/div/ul/a[5]/li')
        journalText = self.driver.find_element_by_xpath('//*[@id="app"]/section/section/aside/div/ul/a[5]/li/span')
        allof = self.driver.find_element_by_xpath('//div[@id="tab-1"]')
        allofText = self.driver.find_element_by_xpath('//div[@id="tab-1"]/div/span')
        self.assertEqual(journalText.text, '日志')  #验证返回界面
        self.assertIn('menu-item-select',journal.get_attribute('class'))
        self.assertEqual(allofText.text, '全部')  #验证返回全部页面
        self.assertEqual('true',allof.get_attribute('aria-selected'))

    def testLog006(self):
        '''验证明天工作内容框输入字母，提示是否正确，返回日志页面'''
        Mylogin(self.driver).login()
        Mylogin(self.driver).mklog()
        self.driver.find_element_by_xpath("//div[@class='form']/div[2]/div/textarea").send_keys(mkstr.letters(10))#输入字母
        self.driver.find_element_by_xpath("//div[@class='el-card__body']/div/div/button[1]/span").click()
        try:
            self.driver.implicitly_wait(10)
            makeText = self.driver.find_element_by_xpath("//div[@role='alert']/p")
            self.assertEqual(makeText.text,'新建成功')
            print("提示：新建成功")
        except:
            pass
        WebDriverWait(self.driver, 10, 0.5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/section/section/aside/div/ul/a[5]/li/span')))
        journal = self.driver.find_element_by_xpath('//*[@id="app"]/section/section/aside/div/ul/a[5]/li')
        journalText = self.driver.find_element_by_xpath('//*[@id="app"]/section/section/aside/div/ul/a[5]/li/span')
        allof = self.driver.find_element_by_xpath('//div[@id="tab-1"]')
        allofText = self.driver.find_element_by_xpath('//div[@id="tab-1"]/div/span')
        self.assertEqual(journalText.text, '日志')  #验证返回界面
        self.assertIn('menu-item-select',journal.get_attribute('class'))
        self.assertEqual(allofText.text, '全部')  #验证返回全部页面
        self.assertEqual('true',allof.get_attribute('aria-selected'))

    def testLog007(self):
        '''验证明天工作内容框输入特殊符号，提示是否正确，返回日志页面'''
        Mylogin(self.driver).login()
        Mylogin(self.driver).mklog()
        self.driver.find_element_by_xpath("//div[@class='form']/div[2]/div/textarea").send_keys(mkstr.spechara(10))#输入特殊符号
        self.driver.find_element_by_xpath("//div[@class='el-card__body']/div/div/button[1]/span").click()
        try:
            self.driver.implicitly_wait(10)
            makeText = self.driver.find_element_by_xpath("//div[@role='alert']/p")
            self.assertEqual(makeText.text,'新建成功')
            print("提示：新建成功")
        except:
            pass
        WebDriverWait(self.driver, 10, 0.5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/section/section/aside/div/ul/a[5]/li/span')))
        journal = self.driver.find_element_by_xpath('//*[@id="app"]/section/section/aside/div/ul/a[5]/li')
        journalText = self.driver.find_element_by_xpath('//*[@id="app"]/section/section/aside/div/ul/a[5]/li/span')
        allof = self.driver.find_element_by_xpath('//div[@id="tab-1"]')
        allofText = self.driver.find_element_by_xpath('//div[@id="tab-1"]/div/span')
        self.assertEqual(journalText.text, '日志')  #验证返回界面
        self.assertIn('menu-item-select',journal.get_attribute('class'))
        self.assertEqual(allofText.text, '全部')  #验证返回全部页面
        self.assertEqual('true',allof.get_attribute('aria-selected'))

    def testLog008(self):
        '''验证明天工作内容框输入小于1000字符，提示是否正确，返回日志页面'''
        Mylogin(self.driver).login()
        Mylogin(self.driver).mklog()
        self.driver.find_element_by_xpath("//div[@class='form']/div[2]/div/textarea").send_keys(mkstr.letters(300))#输入300字符
        self.driver.find_element_by_xpath("//div[@class='el-card__body']/div/div/button[1]/span").click()
        try:
            self.driver.implicitly_wait(10)
            makeText = self.driver.find_element_by_xpath("//div[@role='alert']/p")
            self.assertEqual(makeText.text,'新建成功')
            print("提示：新建成功")
        except:
            pass
        WebDriverWait(self.driver, 10, 0.5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/section/section/aside/div/ul/a[5]/li/span')))
        journal = self.driver.find_element_by_xpath('//*[@id="app"]/section/section/aside/div/ul/a[5]/li')
        journalText = self.driver.find_element_by_xpath('//*[@id="app"]/section/section/aside/div/ul/a[5]/li/span')
        allof = self.driver.find_element_by_xpath('//div[@id="tab-1"]')
        allofText = self.driver.find_element_by_xpath('//div[@id="tab-1"]/div/span')
        self.assertEqual(journalText.text, '日志')  #验证返回界面
        self.assertIn('menu-item-select',journal.get_attribute('class'))
        self.assertEqual(allofText.text, '全部')  #验证返回全部页面
        self.assertEqual('true',allof.get_attribute('aria-selected'))

    def testLog009(self):
        '''验证明天工作内容框输入大于1000字符，提示是否正确，返回日志页面'''
        Mylogin(self.driver).login()
        Mylogin(self.driver).mklog()
        url1 = self.driver.current_url
        self.driver.find_element_by_xpath("//div[@class='form']/div[2]/div/textarea").send_keys(mkstr.letters(1400))#输入300字符
        self.driver.find_element_by_xpath("//div[@class='el-card__body']/div/div/button[1]/span").click()
        makeText = self.driver.find_element_by_xpath("/html/body/div[5]/p")
        time.sleep(3)
        url2 = self.driver.current_url
        self.assertEqual(makeText.text, "新建失败")#验证提示信息
        self.assertEqual(url1, url2)  #验证返回界面

    def testLog010(self):
        '''验证明天工作内容框输入999字符，提示是否正确，返回日志页面'''
        Mylogin(self.driver).login()
        Mylogin(self.driver).mklog()
        self.driver.find_element_by_xpath("//div[@class='form']/div[2]/div/textarea").send_keys(mkstr.letters(999))#输入999字符
        self.driver.find_element_by_xpath("//div[@class='el-card__body']/div/div/button[1]/span").click()
        try:
            self.driver.implicitly_wait(10)
            makeText = self.driver.find_element_by_xpath("//div[@role='alert']/p")
            self.assertEqual(makeText.text,'新建成功')
            print("提示：新建成功")
        except:
            pass
        WebDriverWait(self.driver, 10, 0.5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/section/section/aside/div/ul/a[5]/li/span')))
        journal = self.driver.find_element_by_xpath('//*[@id="app"]/section/section/aside/div/ul/a[5]/li')
        journalText = self.driver.find_element_by_xpath('//*[@id="app"]/section/section/aside/div/ul/a[5]/li/span')
        allof = self.driver.find_element_by_xpath('//div[@id="tab-1"]')
        allofText = self.driver.find_element_by_xpath('//div[@id="tab-1"]/div/span')
        self.assertEqual(journalText.text, '日志')  #验证返回日志界面
        self.assertIn('menu-item-select',journal.get_attribute('class'))
        self.assertEqual(allofText.text, '全部')  #验证返回全部页面
        self.assertEqual('true',allof.get_attribute('aria-selected'))

    def testLog011(self):
        '''验证明天工作内容框输入1000字符，提示是否正确，返回日志页面'''
        Mylogin(self.driver).login()
        Mylogin(self.driver).mklog()
        self.driver.find_element_by_xpath("//div[@class='form']/div[2]/div/textarea").send_keys(mkstr.letters(1000))#输入1000字符
        self.driver.find_element_by_xpath("//div[@class='el-card__body']/div/div/button[1]/span").click()
        WebDriverWait(self.driver, 10, 0.5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/section/section/aside/div/ul/a[5]/li/span')))#定位日志页面
        try:
            self.driver.implicitly_wait(5)
            makeText = self.driver.find_element_by_xpath("//div[@role='alert']/p")
            self.assertEqual(makeText.text,'新建成功')
            print("提示：新建成功")
        except:
            pass
        journal = self.driver.find_element_by_xpath('//*[@id="app"]/section/section/aside/div/ul/a[5]/li')
        journalText = self.driver.find_element_by_xpath('//*[@id="app"]/section/section/aside/div/ul/a[5]/li/span')
        allof = self.driver.find_element_by_xpath('//div[@id="tab-1"]')
        allofText = self.driver.find_element_by_xpath('//div[@id="tab-1"]/div/span')
        self.assertEqual(journalText.text, '日志')  #验证返回日志界面
        self.assertIn('menu-item-select',journal.get_attribute('class'))
        self.assertEqual(allofText.text, '全部')  #验证返回全部页面
        self.assertEqual('true',allof.get_attribute('aria-selected'))

    def testLog012(self):
        '''验证快速创建日志，明天工作内容输入1001个字母，提示是否正确'''
        Mylogin(self.driver).login()
        Mylogin(self.driver).mklog()
        url1 = self.driver.current_url
        self.driver.find_element_by_xpath("//div[@class='form']/div[2]/div/textarea").send_keys(mkstr.letters(1001))#输入1001个字母
        self.driver.find_element_by_xpath("//div[@class='el-card__body']/div/div/button[1]/span").click()
        makeText = self.driver.find_element_by_xpath("/html/body/div[5]/p")
        time.sleep(3)
        url2 = self.driver.current_url
        self.assertEqual(makeText.text, "新建失败")#验证提示信息
        self.assertEqual(url1, url2)  #验证返回界面

    def testLog013(self):
        '''验证上传图片，提示是否正确，返回日志页面'''
        Mylogin(self.driver).login()
        Mylogin(self.driver).mklog()
        self.driver.find_element_by_xpath("//div[@class='form']/div[1]/div/textarea").send_keys('今天工作内容是拜访客服')#输入汉字
        for i in range(0,8):
            actions = ActionChains(self.driver).send_keys(Keys.TAB).perform() #8次TAB，下划到底部
        self.driver.find_element_by_css_selector('div.el-upload.el-upload--picture-card>input').send_keys(r'C:\Users\wu\Desktop\test.png')
        self.driver.implicitly_wait(5)
        pictureClass = self.driver.find_element_by_xpath('//div[@class="form"]/div[4]/div/div/ul/li')
        self.assertTrue(pictureClass.is_displayed())
        time.sleep(3)
        self.driver.find_element_by_xpath("//div[@class='el-card__body']/div/div/button[1]/span").click()
        try:
            self.driver.implicitly_wait(10)
            makeText = self.driver.find_element_by_xpath("//div[@role='alert']/p")
            self.assertEqual(makeText.text,'新建成功')
            print("提示：新建成功")
        except:
            pass
        WebDriverWait(self.driver, 10, 0.5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/section/section/aside/div/ul/a[5]/li/span')))
        journal = self.driver.find_element_by_xpath('//*[@id="app"]/section/section/aside/div/ul/a[5]/li')
        journalText = self.driver.find_element_by_xpath('//*[@id="app"]/section/section/aside/div/ul/a[5]/li/span')
        allof = self.driver.find_element_by_xpath('//div[@id="tab-1"]')
        allofText = self.driver.find_element_by_xpath('//div[@id="tab-1"]/div/span')
        self.assertEqual(journalText.text, '日志')  #验证返回日志界面
        self.assertIn('menu-item-select',journal.get_attribute('class'))
        self.assertEqual(allofText.text, '全部')  #验证返回全部页面
        self.assertEqual('true',allof.get_attribute('aria-selected'))

    def testLog014(self):
        '''验证新建日志上传1张图片后用delete删除图片'''
        Mylogin(self.driver).login()
        Mylogin(self.driver).mklog()
        self.driver.find_element_by_xpath("//div[@class='form']/div[1]/div/textarea").send_keys(
            '今天工作内容是拜访客服')  # 输入汉字
        for i in range(0, 8):
            actions = ActionChains(self.driver).send_keys(Keys.TAB).perform()  # 8次TAB，下划到底部
        self.driver.find_element_by_css_selector('div.el-upload.el-upload--picture-card>input').send_keys(
            r'C:\Users\wu\Desktop\test.png')#上传图片
        self.driver.implicitly_wait(5)
        picture = self.driver.find_element_by_xpath('//div[@class="form"]/div[4]/div/div/ul/li')#定位图片
        time.sleep(3)
        picture.click()#点击图片
        ActionChains(self.driver).send_keys(Keys.DELETE).perform()#键盘按delete
        self.driver.implicitly_wait(5)
        self.driver.find_element_by_xpath('//div[@role="dialog"]/div/div/button[2]/span').click()#点击确定
        makeText = self.driver.find_element_by_xpath("/html/body/div[5]/p")
        time.sleep(3)
        self.assertEqual(makeText.text,'操作成功')#验证提示信息
        try:
            self.driver.find_element_by_xpath('//div[@class="form"]/div[4]/div/div/ul/li')
        except:
            print('图片已删除')#验证图片是否删除

    def testLog015(self):
        '''验证新建日志上传1张图片后点击删除图片'''
        Mylogin(self.driver).login()
        Mylogin(self.driver).mklog()
        self.driver.find_element_by_xpath("//div[@class='form']/div[1]/div/textarea").send_keys(
            '今天工作内容是拜访客服')  # 输入汉字
        for i in range(0, 8):
            ActionChains(self.driver).send_keys(Keys.TAB).perform()  # 8次TAB，下划到底部
        self.driver.find_element_by_css_selector('div.el-upload.el-upload--picture-card>input').send_keys(
            r'C:\Users\wu\Desktop\test.png')#上传图片
        self.driver.implicitly_wait(5)
        ele = self.driver.find_element_by_xpath('//div[@class="form"]/div[4]/div/div/ul/li')#定位图片
        ActionChains(self.driver).move_to_element(ele).perform()
        time.sleep(2)
        self.driver.find_element_by_xpath('//div[@class="form"]/div[4]/div/div/ul/li/span/span[2]/i').click()#点击删除
        self.driver.implicitly_wait(5)
        self.driver.find_element_by_xpath('//div[@role="dialog"]/div/div/button[2]/span').click()#点击确定
        makeText = self.driver.find_element_by_xpath("/html/body/div[5]/p")
        time.sleep(3)
        self.assertEqual(makeText.text,'操作成功')#验证提示信息
        try:
            self.driver.find_element_by_xpath('//div[@class="form"]/div[4]/div/div/ul/li')
        except:
            print('图片已删除')#验证图片是否删除

    def testLog016(self):
        '''验证新建日志上传1张图片后用取消删除图片'''
        Mylogin(self.driver).login()
        Mylogin(self.driver).mklog()
        self.driver.find_element_by_xpath("//div[@class='form']/div[1]/div/textarea").send_keys(
            '今天工作内容是拜访客服')  # 输入汉字
        for i in range(0, 8):
            ActionChains(self.driver).send_keys(Keys.TAB).perform()  # 8次TAB，下划到底部
        self.driver.find_element_by_css_selector('div.el-upload.el-upload--picture-card>input').send_keys(
            r'C:\Users\wu\Desktop\test.png')#上传图片
        self.driver.implicitly_wait(5)
        ele = self.driver.find_element_by_xpath('//div[@class="form"]/div[4]/div/div/ul/li')#定位图片
        ActionChains(self.driver).move_to_element(ele).perform()
        time.sleep(2)
        self.driver.find_element_by_xpath('//div[@class="form"]/div[4]/div/div/ul/li/span/span[2]/i').click()#点击删除
        self.driver.implicitly_wait(5)
        self.driver.find_element_by_xpath('//div[@role="dialog"]/div/div/button[1]/span').click()#点击取消
        makeText = self.driver.find_element_by_xpath("/html/body/div[5]/p")
        time.sleep(3)
        self.assertEqual(makeText.text,'已取消操作')#验证提示信息
        self.assertIsNotNone(self.driver.find_element_by_xpath('//div[@class="form"]/div[4]/div/div/ul/li'),'图片未删除')#验证图片是否删除

    def testLog017(self):
        '''验证上传附件 ，提示是否正确，返回日志页面'''
        Mylogin(self.driver).login()
        Mylogin(self.driver).mklog()
        self.driver.find_element_by_xpath("//div[@class='form']/div[1]/div/textarea").send_keys('今天工作内容是拜访客服')#输入汉字
        for i in range(0,8):
            actions = ActionChains(self.driver).send_keys(Keys.TAB).perform() #8次TAB，下划到底部
        self.driver.find_element_by_css_selector('div.el-upload.el-upload--text>input').send_keys(r'C:\Users\wu\Desktop\test.png')#上传附件
        self.driver.implicitly_wait(5)
        picture = self.driver.find_element_by_xpath('//div[@class="form"]/div[4]/p/div/ul/li')
        self.assertTrue(picture.is_displayed())#验证上传附件是否显示
        time.sleep(3)
        self.driver.find_element_by_xpath("//div[@class='el-card__body']/div/div/button[1]/span").click()#点击提交
        try:
            self.driver.implicitly_wait(10)
            makeText = self.driver.find_element_by_xpath("//div[@role='alert']/p")
            self.assertEqual(makeText.text,'新建成功')
            print("提示：新建成功")
        except:
            pass
        WebDriverWait(self.driver, 10, 0.5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/section/section/aside/div/ul/a[5]/li/span')))
        journal = self.driver.find_element_by_xpath('//*[@id="app"]/section/section/aside/div/ul/a[5]/li')
        journalText = self.driver.find_element_by_xpath('//*[@id="app"]/section/section/aside/div/ul/a[5]/li/span')
        allof = self.driver.find_element_by_xpath('//div[@id="tab-1"]')
        allofText = self.driver.find_element_by_xpath('//div[@id="tab-1"]/div/span')
        self.assertEqual(journalText.text, '日志')  #验证返回日志界面
        self.assertIn('menu-item-select',journal.get_attribute('class'))
        self.assertEqual(allofText.text, '全部')  #验证返回全部页面
        self.assertEqual('true',allof.get_attribute('aria-selected'))

    def testLog018(self):
        '''验证新建日志上传1个附件后点击删除图片'''
        Mylogin(self.driver).login()
        Mylogin(self.driver).mklog()
        self.driver.find_element_by_xpath("//div[@class='form']/div[1]/div/textarea").send_keys(
            '今天工作内容是拜访客服')  # 输入汉字
        for i in range(0, 8):
            ActionChains(self.driver).send_keys(Keys.TAB).perform()  # 8次TAB，下划到底部
        self.driver.find_element_by_css_selector('div.el-upload.el-upload--text>input').send_keys(
            r'C:\Users\wu\Desktop\test.png')#上传附件
        self.driver.implicitly_wait(5)
        ele = self.driver.find_element_by_xpath('//div[@class="form"]/div[4]/p/div/ul/li/a')#定位删除附件按钮
        ActionChains(self.driver).move_to_element_with_offset(ele,200,40).perform()
        time.sleep(2)
        self.driver.find_element_by_xpath('//div[@class="form"]/div[4]/p/div/ul/li/i[1]').click()#点击删除
        self.driver.implicitly_wait(5)
        self.driver.find_element_by_xpath('//div[@role="dialog"]/div/div/button[2]/span').click()#点击确定
        makeText = self.driver.find_element_by_xpath("/html/body/div[5]/p")
        time.sleep(3)
        self.assertEqual(makeText.text,'操作成功')#验证提示信息
        try:
            self.driver.find_element_by_xpath('//div[@class="form"]/div[4]/p/div/ul/li')
        except:
            print('附件已删除')#验证附件是否删除

    def testLog019(self):
        '''验证新建日志上传1个附件后点击删除图片'''
        Mylogin(self.driver).login()
        Mylogin(self.driver).mklog()
        self.driver.find_element_by_xpath("//div[@class='form']/div[1]/div/textarea").send_keys(
            '今天工作内容是拜访客服')  # 输入汉字
        for i in range(0, 8):
            ActionChains(self.driver).send_keys(Keys.TAB).perform()  # 8次TAB，下划到底部
        self.driver.find_element_by_css_selector('div.el-upload.el-upload--text>input').send_keys(
            r'C:\Users\wu\Desktop\test.png')#上传附件
        self.driver.implicitly_wait(5)
        ele = self.driver.find_element_by_xpath('//div[@class="form"]/div[4]/p/div/ul/li/a')#定位删除附件按钮
        ActionChains(self.driver).move_to_element_with_offset(ele,200,40).perform()
        time.sleep(5)
        self.driver.find_element_by_xpath('//div[@class="form"]/div[4]/p/div/ul/li/i[1]').click()#点击删除
        self.driver.implicitly_wait(5)
        self.driver.find_element_by_xpath('//div[@role="dialog"]/div/div/button[1]/span').click()#点击取消
        makeText = self.driver.find_element_by_xpath("/html/body/div[5]/p")
        time.sleep(3)
        self.assertEqual(makeText.text,'已取消操作')#验证提示信息
        self.assertIsNotNone(self.driver.find_element_by_xpath('//div[@class="form"]/div[4]/p/div/ul/li'),'附件未删除')#验证附件是否删除

    def testLog020(self):
        '''验证回复日志内容和提示显示'''
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
        time.sleep(2)
        #点击回复提交
        self.driver.find_element_by_xpath('//*[@id="pane-1"]/div[1]/div[2]/div[1]/div[3]/div/textarea/../../div[2]/div/button[1]/span').click()
        WebDriverWait(self.driver, 10, 0.1).until(
            EC.presence_of_element_located((By.XPATH, '//div[@role="alert"]/p')))
        #获取提示内容
        makeText = self.driver.find_element_by_xpath("//div[@role='alert']/p")
        self.assertEqual(makeText.text,'回复成功')
        time.sleep(3)
        #获取所有回复内容
        sendContent = self.driver.find_elements_by_css_selector('.reply-title>span')
        sendContentRawList = []
        for i in range(0, len(sendContent)):
            sendContentRawList.append(sendContent[i].text)
        sendContentList = "".join(sendContentRawList)
        self.assertIn(reply, sendContentList)

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

    def testLog022(self):
        '''验证类型为日报的检索内容是否正确显示'''
        Mylogin(self.driver).login()
        #点击日志
        WebDriverWait(self.driver,20,0.5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/section/section/aside/div/ul/a[5]/li/span')))
        self.driver.find_element_by_xpath('//*[@id="app"]/section/section/aside/div/ul/a[5]/li/span').click()
        WebDriverWait(self.driver, 20, 0.5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="pane-1"]/div[1]/div[2]/div[1]/div[2]/button/span')))
        #点击类型下拉
        self.driver.find_element_by_xpath('//*[@id="pane-1"]/div/div[1]/div[3]/div/div/span/span/i').click()
        time.sleep(3)
        #点击日报
        self.driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/ul/li[2]').click()
        time.sleep(15)
        #获取所有日志内容
        sendContent = self.driver.find_elements_by_css_selector('p.row>span')
        sendContentRawList = []
        for i in range(0, len(sendContent)):
            sendContentRawList.append(sendContent[i].text)
        sendContentList = "".join(sendContentRawList)
        self.assertNotIn('本周工作内容：', sendContentList)
        self.assertNotIn('本月工作内容：', sendContentList)
        self.assertIn('今日工作内容：', sendContentList)


if __name__ == "__main__":
    unittest.main()