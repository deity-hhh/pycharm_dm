import requests
from bs4 import BeautifulSoup
import csv
url="http://www.baidu.com"
resp=requests.get(url)

f=open("表格.csv","w",encoding="utf-8")
csvwriter=csv.writer(f)

#print(resp.text)
#将源代码交给beautifulsoup
page=BeautifulSoup(resp.text,"html.parser")  #指定html解释器
#查找数据---find(标签，属性=值） 或 find_all(标签，属性=值）
#table=page.find("table",class_="hhhhh")   #class是关键字,加一个下划线可以避免报错
table=page.find("table",attrs={"class":"hhhhh"})   #意思同上
#获取所有数据行（tr）
trs=table.find_all("tr")[1:]   #用切片除去表头
for tr in trs:     #每一行
    tds=tr.find_all("td")    #每一行所有td
    name=tds[0].text
    low=tds[1].text
    high=tds[2].text
    kind=tds[3].text
    date=tds[4].text
    csvwriter.writerow([name,low,high,kind,date])
f.close()
resp.close()
