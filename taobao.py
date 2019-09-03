import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from config import *
import re
from bs4 import BeautifulSoup
import pymongo

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{CHROME_DEBUG_PORT}")
browser = webdriver.Chrome(chrome_options = chrome_options)
wait = WebDriverWait(browser, 10)

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

def search():
    print('正在搜索：', KEYWORD)
    try:
        url = 'https://s.taobao.com/search?q=' + KEYWORD
        browser.get(url)
        total = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="total"]')))
        total = int(re.search('\d{2,}',total.text).group())
        get_product()
        return total
    except TimeoutError:
        return search()

def next_page(page_number):
    print('正在翻页：', page_number)
    try:
        input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="input J_Input"]')))
        submit = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="btn J_Submit"]')))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="mainsrp-pager"]/div/div/div/ul/li[@class="item active"]/span'), str(page_number)))
        get_product()
    except TimeoutError:
        return next_page(page_number)


def get_product():
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
        html = browser.page_source
        soup = BeautifulSoup(html, 'lxml')
        items = soup.select('#mainsrp-itemlist .items .item')
        for item in items:
            product = {
                'image':item.select('.pic .img')[0].attrs['src'],
                'price':item.select('.price')[0].get_text(),
                'deal':item.select('.deal-cnt')[0].get_text()[:-3],
                'title':item.select('.title')[0].get_text(),
                'shop':item.select('.shop')[0].get_text(),
                'location':item.select('.location')[0].get_text()
            }
            print(product)
            save_to_mongodb(product)
    except TimeoutError:
        return get_product()

def save_to_mongodb(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('存储到MONGODB成功', result)
    except Exception:
        print('存储到MONGODB失败', result)



if __name__ == '__main__':
    try:
        total = search()
        for i in range(2, total + 1):
            try:
                next_page(i)
            except:
                print("请手动滑动验证码！")
                time.sleep(20)
                next_page(i)
    except Exception:
        print('出错啦')
    finally:
        browser.close()