# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2017-11-10 Friday
# @email: i@yanshengjia.com


from time import sleep
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import codecs
import json


class ZhixueCrawler():
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.current_report_id = 1
        self.report_id_min = 1
        self.report_id_max = 10
        self.current_page_id = 1
        self.page_id_min = 1
        self.page_id_max = 70
        self.data = []

    # guest login -> click "智作文" -> click "我的作文" -> click "英语"
    def login(self):
        zhixue_url = "http://www.zhixue.com/demoLogin/"
        self.browser.get(zhixue_url)
        self.browser.implicitly_wait(10)
        button_smart_essay = self.browser.find_element_by_xpath("//*[@id='head_menuList']/li[4]/a")
        button_smart_essay.click()
        sleep(2)
        button_my_essay = self.browser.find_element_by_xpath("/html/body/div[3]/div[1]/ul/li[2]/a")
        button_my_essay.click()
        sleep(2)
        button_english = self.browser.find_element_by_xpath("//*[@id='headerSelect']/div[1]/a[3]")
        button_english.click()
        sleep(2)

    # click "查看报告" -> get the essay and the relevent prompt -> go back one page
    # report id: [report_id_min, report_id_max]
    def view_report(self, report_id):
        dict = {}   # {"Page ID": page id, "Report ID": report id, "Prompt": prompt content, "Essay": essay content}
        self.current_report_id = report_id
        report_xpath = "//*[@id='compositionListBox']/div[" + str(report_id) + "]/div[3]/a"
        button_view_report = self.browser.find_element_by_xpath(report_xpath)
        # button_view_report.click()
        ActionChains(self.browser).click(button_view_report).perform()
        sleep(3)

        print 'Page: ' + str(self.current_page_id) + '    Report: ' + str(self.current_report_id)

        # get essay
        element_essay = self.browser.find_element_by_xpath("//*[@id='compositionText']/div[2]/p/span")
        dict['Essay'] = element_essay.text

        # get prompt
        button_view_prompt = self.browser.find_element_by_xpath("//*[@id='lookTopic']")
        button_view_prompt.click()
        sleep(3)
        element_prompt = self.browser.find_element_by_xpath("//*[@id='lookOriginalBox']/div/div[2]/div/div")
        dict['Prompt'] = element_prompt.text

        dict['Page ID'] = self.current_page_id
        dict['Report ID'] = self.current_report_id
        self.data.append(dict)

        self.browser.back()
        sleep(3)

    # page-turning by entering the page id to the "跳转到" input text field
    # page id: [page_id_min, page_id_max]
    def turn_page(self, page_begin, page_end):
        for page_id in range(page_begin, page_end + 1):
            self.current_page_id = page_id
            input_page_id = self.browser.find_element_by_xpath("//*[@id='pagination']/div/input")
            input_page_id.clear()
            input_page_id.send_keys(str(page_id))
            button_go = self.browser.find_element_by_xpath("//*[@id='pagination']/div/button")
            button_go.click()
            sleep(3)
            for report_id in range(self.report_id_min, self.report_id_max + 1):
                self.view_report(report_id)

    def shutdown(self):
        self.browser.close()


def main():
    output_path = '../output/zhixue.txt'
    zhixue_crawler = ZhixueCrawler()
    zhixue_crawler.login()
    zhixue_crawler.turn_page(zhixue_crawler.page_id_min, zhixue_crawler.page_id_max)
    zhixue_crawler.shutdown()

    with codecs.open(output_path, mode='w', encoding='UTF8') as output_file:
        data_json = json.dumps(zhixue_crawler.data, ensure_ascii=False)
        output_file.write(data_json)

if __name__ == '__main__':
    main()
