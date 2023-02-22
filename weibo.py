import requests
import parsel
import csv
import time
import os
import re

#os.environ["http_proxy"] = "http://135.251.33.16:80"
#os.environ["https_proxy"] = "http://135.251.33.16:80"
os.environ["http_proxy"] = "http://10.158.100.9:8080"
os.environ["https_proxy"] = "http://10.158.100.9:8080"
#os.environ["http_proxy"] = "http://135.252.244.221:3128"
#os.environ["https_proxy"] = "http://135.252.244.221:3128"

f = open('./weibo/热榜4.csv', mode='a', encoding='utf-8', newline='')
csv_writer = csv.DictWriter(f, fieldnames=[
    '时间',
    '排名',
    '标题',
    '热度',
])
csv_writer.writeheader()
loop = True

def get_content():
    url = 'https://s.weibo.com/top/summary?cate=realtimehot'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
        'Cookie': 'SINAGLOBAL=1841149334224.8252.1642397316953; SUB=_2AkMVODNxf8NxqwFRmP4dxWjkb4xxzw3EieKjZMKqJRMxHRl-yT9jqhJctRB6PrgdnsJWNs-mEM0FvrXkkj_GbQ92SyMy; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WhUHi5ZivCRoPRwfx_.UyF6; login_sid_t=21ee6d671cc1f4245087df89ce7770b5; cross_origin_proto=SSL; _s_tentry=passport.weibo.com; Apache=1841149334224.8252.1642397316953; ULV=1676516741382:1:1:1:1841149334224.8252.1642397316953:'
    }
    response = requests.get(url=url, headers=headers)
    #print(response)
    selector = parsel.Selector(response.text)
    #print(selector)
    trs = selector.css('#pl_top_realtimehot tbody tr')[:50]

    return trs

while loop:
    now_time = int(time.time())
    timeArray = time.localtime(now_time)
    date = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

    try:
        trs = get_content()
        print(len(trs))

        for tr in trs:
            num = tr.css('td.td-01.ranktop::text').get()
            print(num)
            if num:
                if num.isdigit():
                    title = tr.css('.td-02 a::text').get()
                    hot2 = tr.css('.td-02 span::text').get()
                    hot = re.sub('([^\u0030-\u0039])', '', hot2)
                    dit = {
                        '时间': date,
                        '排名': num,
                        '标题': title,
                        '热度': hot,
                    }
                    print(dit)
                    csv_writer.writerow(dit)
                else:
                    print("not digit num.")
        #loop = False
        time.sleep(120)

    except:
        print('get url failed.')