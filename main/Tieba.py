from selenium import webdriver

import time

class TieBa(object):
    ##初始化##
    def __init__(self):
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        browser = webdriver.Chrome() #无界面Google
        browser.implicitly_wait(30)
        browser.get("https://tieba.baidu.com/f?kw=%BF%B9%D1%B9&fr=ala0&tpl=5")
        self.browser = browser
        self.currentWindow = browser.current_window_handle  #当前窗口句柄
        print("----------浏览器初始化成功----------")
        time.sleep(10)

    ##登录操作##
    def auto_login(self):
        print("----------开始登录----------")
        self.browser.find_element_by_link_text("登录").click()  #登录
        time.sleep(2)
        self.browser.find_element_by_id('TANGRAM__PSP_11__footerULoginBtn').click()  # 切换登陆方式
        username = self.browser.find_element_by_id("TANGRAM__PSP_11__userName")
        username.click()
        username.send_keys("*********")
        password = self.browser.find_element_by_id("TANGRAM__PSP_11__password")
        password.clear()
        password.send_keys("*********")
        self.browser.find_element_by_id("TANGRAM__PSP_11__submit").click()  # 点击登录
        time.sleep(3)
        if self.is_Element_Exist('dialogJclose'):  # 关闭弹窗
            self.browser.find_element_by_class_name("dialogJclose").click()
            time.sleep(2)
        print("----------登录成功----------")

    ##窗口切换##
    def switch_window(self):
        handles = self.browser.window_handles #获取所有窗口句柄
        for handle in handles:
            if handle != self.currentWindow:
                self.browser.switch_to_window(handle) #切换到新窗口

    #用来确认元素是否存在，如果存在返回flag=true，否则返回false
    def is_Element_Exist(self,element):
        flag = True
        try:
            self.browser.find_element_by_class_name(element)
            return flag
        except:
            flag = False
            return flag

    ##开始水贴
    def start_post(self):
        print("----------开始水贴----------")
        lis = self.browser.find_elements_by_xpath("//ul[@id='thread_list']/li")
        num = 0
        try:
            for li in lis:
                num += 1
                rep_num = li.find_element_by_class_name("threadlist_rep_num").text
                if (int(rep_num) < 10 and int(rep_num) > 0) or int(rep_num) == 1:
                    href = self.browser.find_element_by_xpath('//*[@id="thread_list"]/li[' + str(num) + ']/div/div[2]/div/div/a')
                    content = href.get_attribute("title")
                    href.click()
                    print("----------点击链接----------")
                    time.sleep(5)
                    self.switch_window() #切换窗口
                    time.sleep(2)
                    self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);") #滚动到最底部,输入框加载完成
                    time.sleep(5)
                    print("----------开始回帖----------")
                    self.browser.find_element_by_id("ueditor_replace").send_keys('机器人测试,请勿回复\n-----------------\n' + content)
                    time.sleep(1)
                    self.browser.find_element_by_class_name("poster_submit").click()
                    time.sleep(5)
                    self.browser.close()
                    print("----------成功回帖----------")
                    time.sleep(4)
                    self.browser.switch_to_window(self.currentWindow)  #切换回原始窗口
                    time.sleep(15)
                else:
                    continue
            print("----------本次回帖" + num + "次----------")
        except Exception as e:
            print(e)
            print("----------异常中断----------")
            return


tieba = TieBa()
tieba.auto_login()
while True:
    tieba.start_post()
    time.sleep(60)
    tieba.browser.refresh()
    time.sleep(15)