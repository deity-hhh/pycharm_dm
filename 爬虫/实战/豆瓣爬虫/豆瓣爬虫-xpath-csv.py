import requests
from lxml import etree
import csv
import time
import random
import re
import os
import os.path


#获得所有电影url
def movie(page_url):
    urls=[]
    page_resp=requests.get(page_url,headers=headers)
    page_resp.encoding='utf-8'
    text=etree.HTML(page_resp.text)
    for i in range(1, 26):
        url_list=text.xpath(f'//*[@id="content"]/div/div[1]/ol/li[{i}]/div/div[2]/div[1]/a/@href')
        if url_list:
            url=url_list[0]
            urls.append(url)
    return urls

#获取电影内容
def content(movie_url):
    resp = requests.get(movie_url, headers=headers)
    resp.encoding = 'utf-8'
    soup = etree.HTML(resp.text)
    rank = soup.xpath('//*[@id="content"]/div[1]/span[1]/text()')[0].strip()
    rank=re.findall(r'\d+',rank)
    name = soup.xpath('//*[@id="content"]/h1/span[1]/text()')[0].strip()
    year = soup.xpath('//*[@id="content"]/h1/span[2]/text()')[0].strip('()')
    director = soup.xpath('//*[@id="info"]/span[1]/span[2]/a/text()')[0].strip()
    actors = soup.xpath('//div[@id="info"]/span[3]//span[@class="attrs"]//a/text()')
    actors_str = '/'.join(actors)
    movie_type = soup.xpath('//span[@property="v:genre"]/text()')
    movie_type_str = '/'.join(movie_type)
    country = soup.xpath('//div[@id="info"]/span[@class="pl" and contains(text(), "制片国家/地区:")]/following-sibling::text()[1]')[0].strip()
    language = soup.xpath('//div[@id="info"]/span[@class="pl" and contains(text(), "语言:")]/following-sibling::text()[1]')[0].strip()
    release_date = soup.xpath('//div[@id="info"]//span[@class="pl" and contains(text(), "上映日期:")]/following-sibling::span[@property="v:initialReleaseDate"]/text()')[0].strip()
    duration = soup.xpath('//div[@id="info"]//span[@class="pl" and contains(text(), "片长:")]/following-sibling::span[@property="v:runtime"]/text()')[0].strip()
    aka_list = soup.xpath(
        '//div[@id="info"]//span[@class="pl" and contains(text(), "又名:")]/following-sibling::text()[1]')
    if aka_list:
        aka = aka_list[0].strip()
    else:
        aka = '无'
    score = soup.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()')[0].strip()
    score_people = soup.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/div/div[2]/a/span/text()')[0].strip()
    five_star = soup.xpath('//*[@id="interest_sectl"]/div[1]/div[3]/div[1]/span[2]/text()')[0].strip()
    four_star = soup.xpath('//*[@id="interest_sectl"]/div[1]/div[3]/div[2]/span[2]/text()')[0].strip()
    three_star = soup.xpath('//*[@id="interest_sectl"]/div[1]/div[3]/div[3]/span[2]/text()')[0].strip()
    two_star = soup.xpath('//*[@id="interest_sectl"]/div[1]/div[3]/div[4]/span[2]/text()')[0].strip()
    one_star = soup.xpath('//*[@id="interest_sectl"]/div[1]/div[3]/div[5]/span[2]/text()')[0].strip()
    summary_title = soup.xpath('//*[@id="content"]/div[2]/div[1]/div[3]/h2/i/text()')[0].strip()
    summary_lst = soup.xpath('//*[@property="v:summary"]//text()')
    if summary_lst:
        summary_lst2 = []
        for text in summary_lst:
            summary_lst2.append(text.strip())
        summary = ''.join(summary_lst2)
    else:
        summary='暂无剧情简介'
    return {
        'rank':rank,
        'name':name,
        'year':year,
        'director':director,
        'actors':actors_str,
        'movie_type':movie_type_str,
        'country':country,
        'language':language,
        'release_date':release_date,
        'duration':duration,
        'aka':aka,
        'score':score,
        'score_people':score_people,
        'five_star':five_star,
        'four_star':four_star,
        'three_star':three_star,
        'two_star':two_star,
        'one_star':one_star,
        'summary_title':summary_title,
        'summary':summary
    }

#存储数据
def save_csv(all_data):
    with open('college_rank.csv','w',newline='',encoding='utf-8') as f:
        csvwriter=csv.writer(f)
        csvwriter.writerow(all_data[0].keys())
        for data in all_data:
            csvwriter.writerow(data.values())

if __name__ == '__main__':
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language':'zh-CN,zh;q=0.9'
    }
    all_data=[]
    for i in range(1):
        page = i * 25
        page_url = f'https://movie.douban.com/top250?start={page}&filter='
        movie_urls = movie(page_url)
        for url in movie_urls:
            movie_data=content(url)
            all_data.append(movie_data)
            time.sleep(random.uniform(1, 3))
    save_csv(all_data)
    print('over!')