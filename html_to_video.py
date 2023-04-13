from selenium import webdriver
import time
import argparse
from module_logger import get_logme

logger = get_logme()


#service = Service(executable_path="~/chrome/chromedriver")
#driver = webdriver.Chrome(service=service)

def html_to_video(filename, interval):
    # 创建chrome选项
    chrome_options = webdriver.ChromeOptions()

    # 启用无头模式
    chrome_options.add_argument('--headless')

    # 创建webdriver实例
    #service = Service(executable_path="~/chrome/chromedriver")
    #browser = webdriver.Chrome(options=chrome_options, executable_path="/home/iawes/chrome/chromedriver")
    browser = webdriver.Chrome(options=chrome_options)

    # 设置要访问的URL
    #url = "https://www.baidu.com"
    #url = "file:////home/iawes/pyhon-crawler/weibo/2023-03-30.video.html"

    # 打开网页
    browser.get(filename)

    time.sleep(interval)

    # 接下来可以进行网页操作，例如提取内容、点击按钮等。
    # 例如：content = browser.find_element_by_id("element_id").text

    # 关闭webdriver实例
    browser.quit()


def train_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", default='./weibo/2023-03-29.video.html', type=str, help='video file path')
    parser.add_argument("--interval", default=300, type=int, help='download time')
    opt = parser.parse_args()
    return opt

if __name__ == "__main__":
    opt = train_options()
    logger.debug(opt)

    try:
        html_to_video(opt.file, opt.interval)
    except:
        logger.exception('html_to_video failed.')