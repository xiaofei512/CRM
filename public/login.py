import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Mylogin(object):
    def __init__(self, driver):
        self.driver = driver

    def login(self):
        WebDriverWait(self.driver, 50, 0.5).until(
            EC.presence_of_element_located((By.NAME, 'username')))
        self.driver.find_element_by_name("username").send_keys("18621796828")
        self.driver.find_element_by_name("password").send_keys("123456")
        self.driver.find_element_by_xpath("//button[@type='button']").click()
        time.sleep(5)
            
    def mklog(self):
        self.driver.implicitly_wait(50)
        ele = self.driver.find_element_by_css_selector('div.button-name')
        ActionChains(self.driver).move_to_element(ele).perform()#鼠标悬停到快速创建
        WebDriverWait(self.driver, 10, 0.5).until(EC.presence_of_element_located((By.XPATH,'//*[@class="quick-add"]/div/p[1]/span')))
        self.driver.find_element_by_xpath('//*[@class="quick-add"]/div/p[1]/span').click()#点击日志
        #等待提交按钮显示
        WebDriverWait(self.driver, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, "//div[@class='el-card__body']/div/div/button[1]/span")))


            
    