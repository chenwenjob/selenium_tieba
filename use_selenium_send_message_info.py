# -*- coding: utf-8 -*-
# @Time    : 2022/5/6 12:09
# @File    : use_selenium_send_message_info.py
# @Description: 百度贴吧工具 顶帖小工具
# @Software: PyCharm

from selenium import webdriver
import time
import random
import re


# 获取浏览器信息，有些网站做了自动测试软件过滤，这里需要改一些参数模拟真实场景。
def get_browser(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    # options.add_argument("--no-sandbox") # linux only
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    browser = webdriver.Chrome(options=options)
    browser.execute_cdp_cmd("Network.enable", {})
    browser.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browserClientA"}})
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
                   Object.defineProperty(navigator, 'webdriver', {
                       get: () => undefined
                   })
               """
    })

    browser.get(url)
    return browser


# 获取内容列表
def get_content():
    contents = []
    with open('content.txt', encoding='utf-8') as f:
        for line in f.readlines():
            contents.append(line.strip())
    # 随机取一条内容
    # print(random.choice(contents))
    return contents


# 获取贴吧账号cookies列表
def get_cookies():
    cookies = []
    with open('cookies.txt', encoding='utf-8') as f:
        for line in f.readlines():
            cookies.append(line)
    # 随机取一条cookies
    # print(random.choice(cookies))
    return cookies


# 获取顶贴的贴子列表
def get_tieba_url():
    tieba_urls = []
    with open('tieba_url.txt', encoding='utf-8') as f:
        for line in f.readlines():
            tieba_urls.append(line.strip())
    return tieba_urls


def main(count, laytime):
    url = "https://tieba.baidu.com/p/7794873792"

    browser = get_browser(url)
    urls = get_tieba_url()
    contents = get_content()
    all_cookies = get_cookies()

    print("=================================")
    print("本次需要顶贴数量为: %s 个;\n账号cookies 数量为: %s 个;\n总循环次数为: %s 条;\n评论列表数目：%s条。" % (
    len(urls), len(all_cookies), count, len(contents)))
    print("=================================")
    sum = 0
    while count > 0:
        for url in urls:
            # cookies资源库中随机取一个cookie
            full_cookies = random.choice(all_cookies).strip().split(":::")
            # full_cookies = all_cookies[1].strip().split(":::")
            cookies = full_cookies[1]
            account = full_cookies[0]
            # 随机取一条内容进行评论
            content = random.choice(contents)
            # 替换cookies
            browser.delete_all_cookies()
            time.sleep(3)
            cookiesList = re.findall(r'([\S\s]*?)=([\S\s]*?);', cookies)
            for cookie in cookiesList:
                ck = {'name': cookie[0].strip(), 'value': cookie[1].strip()}
                browser.add_cookie(ck)
            browser.get(url)
            time.sleep(3)
            # 滑动到底端
            browser.execute_script("var q=document.documentElement.scrollTop=10000")
            print("获取了的贴子: %s ; 使用账号: '%s' 开始顶贴评论。" % (url, account))

            # 书写评论内容
            js = "document.getElementById('ueditor_replace').innerHTML='%s'" % content
            browser.execute_script(js)
            time.sleep(2)
            # 提交评论
            browser.find_element_by_class_name('poster_submit').click()
            time.sleep(laytime)
        count = count - 1
        sum = sum + 1
        print("第 %s 次循环,还省 %s 次循环。" % (sum, count))

    browser.close()
    browser.quit()


if __name__ == '__main__':
    # 第一参数 循环次数。 第二个参数 评论间隔时间 秒。
    main(4, 5)
