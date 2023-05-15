# 导入requests库和BeautifulSoup库
import requests
from bs4 import BeautifulSoup

# 定义一个函数，获取雪球热榜的网页内容
def get_xueqiu_hotlist():
    # 设置请求头，模拟浏览器访问
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        # 添加cookie，这里是从浏览器中复制的一个示例，你需要替换成你自己的cookie
        "Cookie": "s=9y1q1ltoso; cookiesu=871683857430251; device_id=a7ab63ee5f26c19165d2620f7b43f18d; Hm_lvt_1db88642e346389874251b5a1eded6e3=1683857432; xq_a_token=8f74549812ba58486ddc81ef1ad6849bd84aa13a; xqat=8f74549812ba58486ddc81ef1ad6849bd84aa13a; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjMyOTc5MDIyMTYsImlzcyI6InVjIiwiZXhwIjoxNjg0NDYyNTY5LCJjdG0iOjE2ODM4NTc2NzMwNTQsImNpZCI6ImQ5ZDBuNEFadXAifQ.P4AAijBCGycy_TAzY7cMJ3IUhVI4kjSCvI9I4UGwrArfsfZ5nGw5EgB2ym_llSt3qcX0_mi7jHCf5KsfW91_VWEkPKZk80ZU9dwSl5fZ5sxdar9ry07Zw7FXw9fU5yzCi-hs1gjC2JtlPz9IaWetRPE-sNzf4Ndbrc11-4QzVxs_TjYU1SDt1v6tNxh8qCrIV87ku5YeBvOmD6FDuqisOuj69SQpmrkIFwkTbXHS0xcD4F5wkZGqUpZik3y1QywGnlNXVepMMROXtNLw033UHUvSe-YXpi-apFclpMMCLg2gGFTSRnSa9zIgp_Se5AiJ2Kd6NhA6jgAC8sWYsQtb4Q; xq_r_token=28087ebbb28e07a0bd7388a53976c7eb64957ba6; xq_is_login=1; u=3297902216; is_overseas=0; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1683857675"
    }
    # 设置请求的url，这里是雪球热榜的首页
    url = "https://xueqiu.com/hots/topic"
    # 发送get请求，获取网页内容
    response = requests.get(url, headers=headers)
    # 判断响应状态码是否为200，表示成功
    if response.status_code == 200:
        # 返回网页内容的文本格式
        return response.text
    else:
        # 返回空字符串
        return ""

# 定义一个函数，解析雪球热榜的网页内容，提取每日热榜的标题和链接
def parse_xueqiu_hotlist(html):
    # 创建一个空列表，用于存储每日热榜的信息
    hotlist = []
    # 使用BeautifulSoup库解析网页内容
    soup = BeautifulSoup(html, "lxml")
    # 找到每日热榜的div标签，class属性为"hot-list-item"
    divs = soup.find_all("div", class_="hot-list-item")
    # 遍历每个div标签
    for div in divs:
        # 找到div标签下的a标签，获取标题和链接
        a = div.find("a")
        title = a.get_text().strip()
        link = a["href"]
        # 将标题和链接组成一个元组，添加到列表中
        hotlist.append((title, link))
    # 返回列表
    return hotlist

# 定义一个函数，打印每日热榜的信息
def print_xueqiu_hotlist(hotlist):
    # 遍历列表中的每个元组
    for title, link in hotlist:
        # 打印标题和链接，用制表符分隔
        print(title, "\t", link)

# 调用函数，获取每日雪球热榜的信息并打印
html = get_xueqiu_hotlist()
hotlist = parse_xueqiu_hotlist(html)
print_xueqiu_hotlist(hotlist)

