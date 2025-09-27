import requests
import re
#获取页面源代码
domain="https://dytt001.com/"
resp=requests.get(domain)
#resp=requests.get(domain,verify=False)    若有防火墙/安全证书等，verify=False可以去掉安全验证
resp.encoding='utf-8'          #根据源代码中 charset="UTF-8" 可知
#print(resp.text)

#获取子页面链接
obj1=re.compile(r'今日热门电影推荐.*?<ul class="ul-imgtxt1 row">(?P<site>.*?)</ul>',re.S)
obj2=re.compile(r'<a href="(?P<href>.*?)">',re.S)
obj3=re.compile(r'<p>◎片　　名　(?P<name>.*?)</p>.*?<p>◎豆瓣链接　(?P<ul>.*?)</p>',re.S)
result=obj1.finditer(resp.text)
child_href_lst=[]
for i in result:
    #print(i.group("site"))
    #提取子页面链接：
    result2=obj2.finditer(i.group("site"))
    for j in result2:
        #print(j.group("href"))
        #拼接子页面的url地址：域名+子页面地址
        child_href=domain+j.group('href').strip("/")
        child_href_lst.append(child_href)   #把子页面链接保存起来

#提取子页面内容--请求地址
for href in child_href_lst:
    child_resp=requests.get(href)
    #print(child_resp.text)
    result3=obj3.finditer(child_resp.text)
    for m in result3:
        print(m.group("name"))
        print(m.group("ul"))
    child_resp.close()
resp.close()
