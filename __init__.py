import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urlparse, parse_qs
import requests
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome('chromedriver.exe', options=options)


def root_li_ret():
    root_select_ul = driver.find_element(By.CSS_SELECTOR,
                                         '#back > div > div.col-sm-12.col-md-12.col-xl-8.col-lg-8 > div:nth-child(2) > div.settle_div > div.jobName_div.col-sm-12.col-md-12.col-lg-12.col-xl-12 > ul')
    select_li_list = root_select_ul.find_elements(By.TAG_NAME, 'li')
    return select_li_list


def sub_li_ret():
    sub_tab_list = driver.find_element(By.CSS_SELECTOR,
                                       '#back > div > div.col-sm-12.col-md-12.col-xl-8.col-lg-8 > div:nth-child(2) > div.settle_div > div.select_div.col-sm-12.col-md-12.col-lg-12.col-xl-12 > ul')
    sub_tab_list_true = sub_tab_list.find_elements(By.TAG_NAME, 'li')
    return sub_tab_list_true


if __name__ == '__main__':

    driver.get("https://dunfaoff.com/ranking.df")

    while True:
        try:
            select_li_list_size = len(root_li_ret())

            print("root_ul_list ", select_li_list_size)

            for root_index in range(0, select_li_list_size):
                li = root_li_ret()[root_index]
                print("root_index ", (root_index + 1), " / ", select_li_list_size)

                data_gb = li.get_attribute('data-sex') + li.get_attribute('data-job')
                print("data_gb ", data_gb)

                li.click()
                time.sleep(0.5)

                select_li_list_size_ch = len(sub_li_ret())
                print("sub_ul_list ", select_li_list_size_ch)
                for sub_index in range(0, select_li_list_size_ch):
                    print("sub_index ", (sub_index + 1), " / ", select_li_list_size_ch)
                    sub_li = sub_li_ret()[sub_index]
                    data_detail_gb = sub_li.get_attribute('data-id')
                    print("data_detail_gb ", data_detail_gb)
                    sub_li.click()
                    time.sleep(0.5)
                    print('sub_li 클릭')
                    search_btn = driver.find_element(By.ID, 'searchbtn')
                    search_btn.send_keys(Keys.RETURN)
                    print('search_btn 클릭')
                    time.sleep(1)
                    imgList = driver.find_elements(By.CLASS_NAME, 'char_img')

                    item_list = []

                    for index in range(0, len(imgList)):
                        imgUrl = imgList[index].get_attribute("src")
                        parse_result = urlparse(imgUrl)
                        requiredList = list(filter(lambda x: x != "",
                                                   parse_result.path.replace("/df/servers/", "\\").replace(
                                                       "/characters/",
                                                       "\\").split(
                                                       "\\")))
                        item_list.append(
                            {"ord_no": index, "server_id": requiredList[0], "ch_id": requiredList[1],
                             "data_gb": data_gb,
                             "data_detail_gb": data_detail_gb})

                    print('request_body: ', item_list)
                    headers = {'Content-Type': 'application/json; charset=utf-8'}
                    response = requests.post("http://localhost:8080/python/insertRanker", json=item_list,
                                             headers=headers)

                    print('response: ', response)
        except Exception as e:
            print(e)
            print("예외가 발생하였습니다 프로그램을 종료하고 5분후 다시 실행합니다")

        time.sleep(300)
