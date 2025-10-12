import requests
from bs4 import BeautifulSoup
import time
import random
import pymysql

#获得所有电影url
def movie(page_url):
    urls=[]
    page_resp=requests.get(page_url,headers=headers)
    page_resp.encoding='utf-8'
    text=BeautifulSoup(page_resp.text,"html.parser")
    hrefs=text.find('ol',class_="grid_view").find_all('div',class_='pic')
    for href in hrefs:
        urls.append(href.find('a')['href'])
    return urls

#获取电影内容
def content(movie_url):
    resp=requests.get(movie_url,headers=headers)
    soup=BeautifulSoup(resp.text,"html.parser")
    rank = soup.find('span',class_="top250-no").text
    name = soup.find('span', property="v:itemreviewed").text
    year = soup.find('span', class_="year").text.strip('()')
    director = soup.find('div', id="info").find('a', rel="v:directedBy").text
    actors_list = soup.find('div', id="info").find_all('a', rel="v:starring")
    if actors_list:
        actors_link = [actor.get_text(strip=True) for actor in actors_list]
        actors = '/'.join(actors_link)
    else:
        actors = '无'
    movie_type_list = soup.find('div', id="info").find_all('span', property="v:genre")
    if movie_type_list:
        link = [actor.get_text(strip=True) for actor in movie_type_list]
        movie_type = '/'.join(link)
    else:
        movie_type = '无'
    country = soup.find('div', id="info").find('span', class_='pl', string='制片国家/地区:').next_sibling.strip()
    language = soup.find('div', id="info").find('span', class_='pl', string='语言:').next_sibling.strip()
    duration = soup.find('div', id="info").find('span', property="v:runtime").text
    aka_string = soup.find('div', id="info").find('span', class_='pl', string='又名:')
    if aka_string:
        aka = aka_string.next_sibling.strip() if aka_string.next_sibling else '无'
    else:
        aka='无'
    score = soup.find('strong', class_="ll rating_num", property="v:average").text
    score_people = soup.find('span', property="v:votes").text
    five_star= soup.find_all('span', class_="rating_per")[0].text
    four_star= soup.find_all('span', class_="rating_per")[1].text
    three_star= soup.find_all('span', class_="rating_per")[2].text
    two_star= soup.find_all('span', class_="rating_per")[3].text
    one_star= soup.find_all('span', class_="rating_per")[4].text
    summary_title = soup.find('div', class_="related-info", style="margin-bottom:-10px;").find('h2').find(
        'i').text.strip()
    summary = soup.find('span', property="v:summary").text.strip()

    return {
        'rank':rank,
        'name':name,
        'year':year,
        'director':director,
        'actors':actors,
        'movie_type':movie_type,
        'country':country,
        'language':language,
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
def save_pymysql(data_list):
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='@xrl1026',
        database='douban_movie',
        charset='utf8'
    )
    cursor = conn.cursor()
    creat_table_sql = "CREATE TABLE IF NOT EXISTS douban_top250(id INT AUTO_INCREMENT PRIMARY KEY,`rank` varchar(255) ,name VARCHAR(200) NOT NULL,year INT,director VARCHAR(100),actors TEXT,movie_type VARCHAR(100),country VARCHAR(50),language VARCHAR(50),duration VARCHAR(50),aka TEXT,score FLOAT,score_people VARCHAR(50),five_star VARCHAR(20),four_star VARCHAR(20),three_star VARCHAR(20),two_star VARCHAR(20),one_star VARCHAR(20),summary_title VARCHAR(50),summary TEXT)"
    cursor.execute(creat_table_sql)
    sql="insert into douban_top250(`rank`, name, year, director, actors, movie_type, country, language,duration, aka,score, score_people, five_star, four_star, three_star, two_star, one_star,summary_title, summary) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    for data in data_list:
        release_date=data['release_date']
        data['release_date'] = release_date[:255] if len(release_date) > 255 else release_date
        cursor.execute(sql,
                       (data['rank'], data['name'], data['year'], data['director'], data['actors'], data['movie_type'],
                        data['country'], data['language'],data['duration'], data['aka'],
                        data['score'], data['score_people'], data['five_star'], data['four_star'],
                        data['three_star'], data['two_star'], data['one_star'], data['summary_title'],
                        data['summary']))
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language':'zh-CN,zh;q=0.9'
    }
    all_data=[]
    for i in range(2):
        page = i * 25
        page_url = f'https://movie.douban.com/top250?start={page}&filter='
        movie_urls = movie(page_url)
        for url in movie_urls:
            movie_data=content(url)
            rank = movie_data['rank']
            if movie_data:
                all_data.append(movie_data)
            time.sleep(random.uniform(1, 3))
    save_pymysql(all_data)
    print('over!')