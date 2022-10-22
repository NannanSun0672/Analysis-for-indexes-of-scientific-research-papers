"""
Creation on  June 21,2019

@author nannan.sun

@Fuction

1. 抓取pubmed 中有关liver fibrosis近5年的临床科研文章标题内容

2. url

"""
import time
import re
import os
import urllib
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

class PubmedInfo(object):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=http://192.168.10.52:1080')
    path ="./chromedriver"
    browser = webdriver.Chrome(path,chrome_options=chrome_options)
    start_url = "https://www.ncbi.nlm.nih.gov/pubmed/P?term="
    #wait = WebDriverWait(browser,10)

    def __init__(self):
        self.key_word = "Liver+cirrhosis"
        self.url = PubmedInfo.start_url + self.key_word
        #self.browser.get(self.url)


    def click_button(self):
        """
        对网页进行模拟点击
        :return:
        """
        self.browser.get(self.url)
        #import IPython
        #IPython.embed()
        #click years
        #time.sleep()
        #button = self.browser.find_element_by_name('fil_val selected')
        #self.wait.until(EC.element_located_to_be_selected((By.XPATH, '//*[@id="Display"]/span[1]')))

        #self.wait.until(
        #    EC.element_to_be_clickable(
        #        (By.XPATH, '//*[@id="Display"]/span[1]'))).click()
        #(By.XPATH, '')
        #year = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#_ds1 > li > ul > li.fil_val.selected > a')))
        #import IPython
        #IPython.embed()
        #year.click()

        # click the numbers of 100 for text
        """
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="Display"]/span[1]'))).click()
        self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#display_settings_menu_ps > fieldset > ul > li:nth-child(5)'))).click()
        #click free full text
        self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#_simsearch > li > ul > li.fil_val.selected > a'))).click()
        #click artical type
        self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#_simsearch > li > ul > li.fil_val.selected > a'))).click()
        """
        print("爬取五年的论文数据，每页显示100条数据......")

    def get_response(self):
        """
        获取页面文档
        :return:
        """
        self.html = self.browser.page_source
        self.doc = etree.HTML(self.html)
    def get_info(self):
        """
            获取列表信息
        :return:
        """
        self.artical_title = self.doc.xpath('//*[@id="maincontent"]/div/div[5]/div[1]/div[2]/p/a/text()')
        self.artical_pmid = self.doc.xpath('//*[@id="maincontent"]/div/div[5]/div[1]/div[2]/div[2]/div/dl/dd/text()')
        self.artical_magizine = self.doc.xpath('//*[@id="maincontent"]/div/div[5]/div[1]/div[2]/div[1]/p[2]/span/text()')
        for pmid in self.artical_pmid:
            print(pmid)
    def next_page(self):
        """
        跳转到下一页
        :return:
        """

        try:
            self.nextpage = self.wait.until(  # 注意这里不是立即点击的，要判断是否可以立即点击
                EC.element_to_be_clickable((By.XPATH, '//*[@id="EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_Pager.Page"]')))
        except TimeoutException:
            self.status = False

    def main(self):
        self.click_button()
        time.sleep(5)
        """
        self.get_response()
        count_pages = 0
        while True:
            self.get_info()
            self.next_page()
            if self.status:
                self.nextpage.click()
                self.get_response()
            else:
                print("跳转未成功")
                break
            count_pages +=1
            print("count_pages",count_pages)
            if count_pages == 2:
                break

            """

if __name__ == "__main__":
    Pubmedinfo = PubmedInfo()
    Pubmedinfo.main()



