
from selenium import webdriver
from urllib.parse import urlparse, parse_qs



options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome('chromedriver.exe', options=options)

if __name__ == '__main__':
    driver.get("https://dunfaoff.com/ranking.df")
    imgUrl = driver.find_element_by_class_name('char_img').get_attribute("src")

    parse_result = urlparse(imgUrl)

    reqList = list(filter(lambda x: x != "", parse_result.path.replace("/df/servers/", "\\").replace("/characters/", "\\").split("\\")))
    dataSet = {"serverId":reqList[0], "itemId":reqList[1]}

    print(dataSet)