# weibo_sc.py

import requests
import parsel
import csv
import time,datetime
import os
import re
import schedule

import argparse
#from loguru import logger
from module_logger import get_logme,add_logme

#import socks
#'proxy_port' should be an integer
#'PROXY_TYPE_SOCKS4' can be replaced to HTTP or PROXY_TYPE_SOCKS5
#socks.setdefaultproxy(socks.PROXY_TYPE_HTTP, "10.158.100.9", 8080)
#socks.wrapmodule(requests)

from weibo_dongtu import new_charts
from weibo_video import convert_video_js
#from html_to_video_2 import html_to_video
#from webm_to_mp4 import webm_to_mp4
from qq_email import qq_send_mail

#logger = MyLogger('.//weibo//').get_logger()
logger = add_logme('.//weibo//')

#def run():
#    print("I'm doing something...")
#
#schedule.every(10).minutes.do(run)    # 每隔十分钟执行一次任务
#schedule.every().hour.do(run)         # 每隔一小时执行一次任务
#schedule.every().day.at("10:30").do(run)  # 每天的10:30执行一次任务
#schedule.every().monday.do(run)  # 每周一的这个时候执行一次任务
#schedule.every().wednesday.at("13:15").do(run) # 每周三13:15执行一次任务
#
#while True:
#    schedule.run_pending()  # run_pending：运行所有可以运行的任务

#os.environ["http_proxy"] = "http://135.251.33.16:80"
#os.environ["https_proxy"] = "http://135.251.33.16:80"
#os.environ["http_proxy"] = "http://10.158.100.9:8080"
#os.environ["https_proxy"] = "http://10.158.100.9:8080"
#os.environ["http_proxy"] = "http://135.252.244.221:3128"
#os.environ["https_proxy"] = "http://135.252.244.221:3128"

#proxies = { "http": "http://10.158.100.9:8080", "https": "http://10.158.100.9:8080", }
#proxies = { "http": "http://135.251.33.16:80", "https": "http://135.251.33.16:80", }

#log
#logger.add("scawler.log", , rotation="7:35")

def get_trs():
    url = 'https://s.weibo.com/top/summary?cate=realtimehot'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'Connection':'close',
        'Cookie': 'SINAGLOBAL=1841149334224.8252.1642397316953; SUB=_2AkMVODNxf8NxqwFRmP4dxWjkb4xxzw3EieKjZMKqJRMxHRl-yT9jqhJctRB6PrgdnsJWNs-mEM0FvrXkkj_GbQ92SyMy; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WhUHi5ZivCRoPRwfx_.UyF6; ULV=1676516741382:1:1:1:1841149334224.8252.1642397316953:; UOR=,,www.baidu.com; login_sid_t=21ee6d671cc1f4245087df89ce7770b5; cross_origin_proto=SSL; _s_tentry=passport.weibo.com; Apache=1841149334224.8252.1642397316953'
    }
    #response = requests.get(url=url, headers=headers, proxies=proxies)
    response = requests.get(url=url, headers=headers)
    #print(response)
    selector = parsel.Selector(response.text)
    #print(selector)
    trs = selector.css('#pl_top_realtimehot tbody tr')[:50]
    return trs

class WeiboHot(object):  # 创建Circle类
    def __init__(self): # 初始化一个属性r（不要忘记self参数，他是类下面所有方法必须的参数）
        self.fd = -1
        self.csv_writer = None
        self.day = '1970-1-1'  # 表示给我们将要创建的实例赋予属性r赋值
        self.csv_file = './weibo/' + self.day + '.csv'
        self.job = None
        self.exist = False
        logger.info('init done.')

    def __del__(self):
        #schedule.clear(self.schedule_tag)
        if self.fd != -1:
            self.fd.close()
        logger.info('clear done.')

    def new_day(self, interval):
        self.day = datetime.date.today().strftime("%Y-%m-%d")
        logger.info('new day %s' %(self.day))
        self.csv_file = './weibo/' + self.day + '.csv'
        logger.debug('new file %s' %(self.csv_file))

        self.new_csv()
        self.process_day(interval)

    def new_csv(self):
        # 判断文件是否存在
        self.exist = os.path.exists(self.csv_file)

        if self.fd != -1:
            self.fd.close()
            self.fd = -1

        self.fd = open(self.csv_file, mode='a', encoding='utf-8', newline='')
        self.csv_writer = csv.DictWriter(self.fd, fieldnames=[
            '时间',
            '排名',
            '标题',
            '热度',
        ])

        if (False == self.exist) :
            self.csv_writer.writeheader()

    def get_content(self):
        now_time = int(time.time())
        timeArray = time.localtime(now_time)
        date = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        try:
            trs = get_trs()
            #print(len(trs))
            for tr in trs:
                num = tr.css('td.td-01.ranktop::text').get()
                #print(num)
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
                        #print(dit)
                        self.csv_writer.writerow(dit)
                    else:
                        logger.warning("not digit num.")
        except:
            logger.exception('get_trs failed.')

    def process_day(self, interval):

#        if self.job != None:
#            schedule.cancel_job(self.job)
#            self.job = None

#        self.job = schedule.every(interval).minutes.do(self.get_content)
         self.job = schedule.every(interval).minutes.until('22:55').do(self.get_content)

        #while True:
        #    schedule.run_pending()

hot = WeiboHot()

def train_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--interval", default=4, type=int, help='interval of timer')
    parser.add_argument("--schedule_on", default=False, type=bool, help='start timer')
    parser.add_argument("--module_on", default=False, type=bool, help='module_on')
    parser.add_argument("--retuest_test", default=False, type=bool, help='retuest_test')
    #parser.add_argument("--max_features", default=6, type=int, help='maximum of features',)
    #parser.add_argument("--max_depth", default=5, type=int,help='maximum depth')
    opt = parser.parse_args()
    return opt

def schedule_day(interval, module_on):
    all_jobs = schedule.get_jobs()
    logger.info(all_jobs)

    hot.new_day(interval)

    all_jobs = schedule.get_jobs()
    logger.info(all_jobs)

    yes = (datetime.datetime.now() + datetime.timedelta(days = -1)).strftime('%Y-%m-%d')
    logger.info(yes)

    weibo_path = os.getcwd()+'/weibo/'
    yes_csv = weibo_path + yes + '.csv'
    yes_echart_html = weibo_path + yes + '.csv.html'
    yes_video_html = weibo_path + yes + '.video.html'

    if (os.path.exists(yes_csv)):
        try:
            new_charts(yes_csv, yes_echart_html)
        except:
            logger.exception('new_charts failed.')

        video_temp = os.getcwd()+'/convert_video_template.html'
        try:
            convert_video_js(yes_echart_html, video_temp, 15, 4, 30, 31, yes_video_html)
        except:
            logger.exception('convert_video_js failed.')

        try:
            qq_send_mail(yes, yes_video_html)
        except:
            logger.exception('qq_send_mail failed.')

#        if module_on == True:
#
#            filename = 'file:///' + yes_video_html
#            print(filename)
#            try:
#                html_to_video(filename, 600)
#            except:
#                print('html_to_video failed.')
#
#            time.sleep(300)
#            webm_path = r'C:\N-20S1PF344DFM-Data\yaweili\Downloads\\' + yes + '.webm'
#            mp4_path = r'C:\N-20S1PF344DFM-Data\yaweili\Downloads\\' + yes + '.mp4'
#            try:
#                webm_to_mp4(webm_path, mp4_path)
#            except:
#                print('webm_to_mp4 failed.')
#
#            time.sleep(300)
#            try:
#                qq_send_mail(yes, mp4_path)
#            except:
#                print('qq_send_mail failed.')

if __name__ == "__main__":

    opt = train_options()
    logger.debug(opt)

    if opt.retuest_test == True:
        get_trs()
        exit()

    # 开始执行任务先
    schedule_day(opt.interval, opt.module_on)

#    if opt.schedule_on == True:
#        # 每天生成新的 csv 和 html
#        schedule.every().day.at("07:30").do(schedule_day, opt.interval)  # 每天的10:30执行一次任务

    all_jobs = schedule.get_jobs()
    logger.info(all_jobs)

    while True:
        schedule.run_pending()
        time.sleep(60)
