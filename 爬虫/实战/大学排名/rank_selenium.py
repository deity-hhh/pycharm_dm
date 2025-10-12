from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import csv
import time

def build():
    t=Options()
    t.add_argument("--no-sandbox")
    t.add_experimental_option('detach',True)
    t.add_argument('--headless')
    t.add_argument('--disable-gpu')

    a=webdriver.Chrome(service=Service('chromedriver.exe'),options=t)
    return a

def one_content(tr):
    rank=tr.find_element(By.XPATH,'./td[1]/div').text.strip()
    name=tr.find_element(By.XPATH,'./td[2]/div/div[2]/div[1]/div/div/span').text.strip()
    english_name=tr.find_element(By.XPATH,'./td[2]/div/div[2]/div[2]/div/div/span').text.strip()
    province=tr.find_element(By.XPATH,'./td[3]').text.strip()
    rating=tr.find_element(By.XPATH,'./td[5]').text.strip()
    educational_level=tr.find_element(By.XPATH,'./td[6]').text.strip()
    return {
        'rank':rank,
        'name':name,
        'english_name':english_name,
        'province':province,
        'rating':rating,
        'educational_level':educational_level
    }
def page_content(net):
    tbody=net.find_elements(By.XPATH,'//*[@id="content-box"]/div[2]/table/tbody/tr')
    page_data=[]
    for t in tbody:
        tr=one_content(t)
        page_data.append(tr)
    return page_data



def save_csv(all_data):
    with open('college_rank.csv','w',newline='',encoding='utf-8') as f:
        csvwriter=csv.writer(f)
        csvwriter.writerow(all_data[0].keys())
        for data in all_data:
            csvwriter.writerow(data.values())

if __name__ == '__main__':
    url='https://www.shanghairanking.cn/rankings/bcur/2024'
    net=build()
    net.get(url)
    all_data=[]
    for i in range(20):
        page_data=page_content(net)
        for data in page_data:
            all_data.append(data)
        if i<19:
            net.find_element(By.XPATH,'//*[@id="content-box"]/ul/li[9]/a').click()
            time.sleep(1)
    net.quit()
    save_csv(all_data)
    print('over!')

