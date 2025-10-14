from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import pymysql

def build():
    t=Options()
    t.add_argument("--no-sandbox")
    t.add_experimental_option('detach',True)
    t.add_argument('--headless')
    t.add_argument('--disable-gpu')

    a=webdriver.Chrome(service=Service('chromedriver.exe'),options=t)
    return a

#获取微博内容及评论
def weibo(net):
    all_weibo=[]     #每个元素都是字典
    all_weibo_comment=[]    #每个元素都是列表（代表一个微博的评论）
    wait=WebDriverWait(net,10)
    wait.until((EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/div[1]/div[1]/div'))))
    #获取微博内容
    for i in range(3):
        time.sleep(3)
        current_divs=net.find_elements(By.XPATH,'//*[@id="app"]/div[1]/div[1]/div')
        if i+3>=len(current_divs):
            continue
        div=current_divs[i+3]
        # 滚动到元素可见
        net.execute_script("arguments[0].scrollIntoView();",div)
        time.sleep(2)

        #信息
        publisher=div.find_element(By.XPATH,'.//header//h3').text.strip()
        publish_time=div.find_element(By.XPATH,'.//header//h4/span[1]').text.strip()
        publish_time=datetime.datetime.strptime(f'2025-{publish_time}','%Y-%m-%d %H:%M')
        web_content=div.find_element(By.XPATH,".//article//div[contains(@class,'weibo-text')]").text.strip()
        form="文字"
        repost_count=div.find_element(By.XPATH,'.//footer/div[1]/h4').text.strip()
        comment_count=div.find_element(By.XPATH,'.//footer/div[2]/h4').text.strip()
        like_count=div.find_element(By.XPATH,'.//footer/div[3]/h4').text.strip()
        one_weibo={
            'publisher':publisher,
            'publish_time':publish_time,
            'form':form,
            'web_content':web_content,
            'repost_count':repost_count,
            'comment_count':comment_count,
            'like_count':like_count
        }
        all_weibo.append(one_weibo)


        #获取该微博评论
        div.find_element(By.XPATH,'.//article').click()
        time.sleep(3)
        # 等待详情页加载
        wait.until(EC.presence_of_element_located((By.TAG_NAME,'body')))
        weibo_comment=comment(net,wait)
        all_weibo_comment.append(weibo_comment)

        #回到原页面
        net.back()
        wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="app"]//div[contains(@class, "card-wrap")]')))
        # 等待页面重新加载
        net.find_element(By.XPATH,'//*[@id="app"]')
    return all_weibo,all_weibo_comment

#获取一条微博的评论
def comment(weibo,wait):
    one_weibo_comment=[]
    wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "comment-content")]')))
    for i in range(10):
        current_comments=wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "comment-content")]/div')))
        c=current_comments[i]
        #滚动到评论可见
        weibo.execute_script("arguments[0].scrollIntoView();",c)
        wait.until(EC.visibility_of(c))  #等待评论完全可见

        commenter=c.find_element(By.XPATH,'.//div[@class="card-main"]//h4').text.strip()
        comment_content=c.find_element(By.XPATH,'.//div[@class="card-main"]//h3').text.strip()
        comment_time=c.find_element(By.XPATH,'.//div[@class="card-main"]//div[@class="m-box-center-a time"]').text.split('来自')[0].strip()
        comment_new_time=datetime.datetime.strptime(f'2025-{comment_time}','%Y-%m-%d %H:%M')
        comment_ip=c.find_element(By.XPATH,'.//div[@class="card-main"]//div[@class="m-box-center-a time"]').text.split('来自')[1].strip()
        one_comment={'commenter':commenter,'comment_ip':comment_ip,'comment_time':comment_new_time.strftime('%Y-%m-%d %H:%M'),'comment_content':comment_content}
        one_weibo_comment.append(one_comment)
    return one_weibo_comment

def save_weibo(all_weibo):
    conn=pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='@xrl1026',
        database='weibo_topic',
        charset='utf8'
    )
    cursor=conn.cursor()
    creat_table_sql="CREATE TABLE IF NOT EXISTS weibo(id INT AUTO_INCREMENT PRIMARY KEY,publisher VARCHAR(200) NOT NULL,publish_time VARCHAR(100),web_content TEXT,form VARCHAR(100),repost_count VARCHAR(50),comment_count VARCHAR(50),like_count VARCHAR(50))"
    cursor.execute(creat_table_sql)
    sql="insert into weibo(publisher,publish_time,web_content,form,repost_count,comment_count,like_count) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    for data in all_weibo:
        cursor.execute(sql,(data['publisher'],data['publish_time'],data['web_content'],data['form'],data['repost_count'],data['comment_count'],data['like_count']))
    conn.commit()
    cursor.close()
    conn.close()

def save_comment(one_weibo_comment):
    conn=pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='@xrl1026',
        database='weibo_topic',
        charset='utf8mb4'
    )
    cursor=conn.cursor()
    creat_table_sql="CREATE TABLE IF NOT EXISTS comment(id INT AUTO_INCREMENT PRIMARY KEY,commenter VARCHAR(200) NOT NULL,comment_ip VARCHAR(100),comment_time VARCHAR(100),comment_content TEXT)"
    cursor.execute(creat_table_sql)
    sql="insert into comment(commenter,comment_ip,comment_time,comment_content) VALUES (%s, %s, %s, %s)"
    for data in one_weibo_comment:
        cursor.execute(sql,(data['commenter'],data['comment_ip'],data['comment_time'],data['comment_content']))
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    url='https://m.weibo.cn/search?containerid=231522type%3D1%26t%3D10%26q%3D%23%E7%83%88%E5%A3%AB%E7%BA%AA%E5%BF%B5%E6%97%A5%23&isnewpage=1&featurecode=newtitle17'
    net=build()
    net.get(url)
    time.sleep(3)
    all_weibo,all_weibo_comment=weibo(net)
    save_weibo(all_weibo)
    for weibo_comment in all_weibo_comment:
        save_comment(weibo_comment)
    print("over!")

