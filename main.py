import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urlparse, parse_qs
import requests


options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome('chromedriver.exe', options=options)

def root_li_ret ():
    root_select_ul = driver.find_element(By.CSS_SELECTOR,'#back > div > div.col-sm-12.col-md-12.col-xl-8.col-lg-8 > div:nth-child(2) > div.settle_div > div.jobName_div.col-sm-12.col-md-12.col-lg-12.col-xl-12 > ul')
    select_li_list = root_select_ul.find_elements(By.TAG_NAME, 'li')
    return select_li_list


def sub_li_ret ():
    sub_tab_list = driver.find_element(By.CSS_SELECTOR,
                                       '#back > div > div.col-sm-12.col-md-12.col-xl-8.col-lg-8 > div:nth-child(2) > div.settle_div > div.select_div.col-sm-12.col-md-12.col-lg-12.col-xl-12 > ul')
    sub_tab_list_true = sub_tab_list.find_elements(By.TAG_NAME, 'li')
    return sub_tab_list_true



if __name__ == '__main__':
    driver.get("https://dunfaoff.com/ranking.df")
    select_li_list_size = len(root_li_ret())

    print("root_ul_list ", select_li_list_size)

    for root_index in range(0, select_li_list_size):
        li = root_li_ret()[root_index]
        print("root_index ", (root_index + 1), " / " ,select_li_list_size)

        data_gb = li.get_attribute('data-sex') + li.get_attribute('data-job')
        print("data_gb ", data_gb)

        li.click()
        time.sleep(3)

        select_li_list_size_ch = len(sub_li_ret())
        print("sub_ul_list ", select_li_list_size_ch)
        for sub_index in range(0, select_li_list_size_ch):
            print("sub_index ", (sub_index + 1), " / ", select_li_list_size_ch)
            sub_li = sub_li_ret()[sub_index]
            data_gb_detail = sub_li.get_attribute('data-id')
            print("data_gb_detail ", data_gb_detail)
            sub_li.click()
            time.sleep(2)
            search_btn = driver.find_element(By.ID, 'searchbtn')
            search_btn.click()
            time.sleep(3)
            imgList = driver.find_elements(By.CLASS_NAME, 'char_img')

            request_body = {}
            item_list = []

            for img in imgList:
                imgUrl = img.get_attribute("src")
                parse_result = urlparse(imgUrl)
                requiredList = list(filter(lambda x: x != "", parse_result.path.replace("/df/servers/", "\\").replace("/characters/","\\").split("\\")))
                item_list.append({"serverId": requiredList[0], "itemId": requiredList[1]})

            request_body['data_gb'] = data_gb
            request_body['data_gb_detail'] = data_gb_detail
            request_body['item_list'] = item_list


            print('request_body: ', request_body)
            headers = {'Content-Type': 'application/json; charset=utf-8'}
            response = requests.post("http://localhost:8080/python/helloWorld", json=request_body, headers=headers)

            print('response: ', response)




