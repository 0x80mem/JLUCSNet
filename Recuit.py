from lxml import etree
import requests
import math
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.options import Options

def work():
    titlexpath = '/html/head/title[1]'
    dics = []
    url = 'https://ccst.jlu.edu.cn/gny.htm'
    pagexpath = '/html/body/div[3]/div[2]/div[2]/div[1]/span[1]'
    patternDrop = re.compile(r'<p[^>]*>|<\/p>|<br>|<br[^>]*>|&nbsp;|<span[^>]*>|'
                             r'</span>|<li[^>]*>|</li>|<ol[^>]*>|<\/ol>|<strong[^>]*>|'
                             r'</strong>|<ul[^>]*>|<\/ul>|<h1[^>]*>|</h1>|<td[^>]*>|</td>|'
                             r'<div[^>]*>|</div>|</form>|<h2[^>]*>|</h2>|<tbody>|<table>|<a[^>]*>|</a>|</tbody>|</table>|\n|\xa0')

    patternStrong = re.compile(r'<strong[^>]*>', re.S)
    options = Options()
    options.use_chromium = True
    options.add_argument('--headless')
    resp = requests.get(url)
    html = etree.HTML(resp.content)
    titles = html.xpath(titlexpath)
    for es in titles:
        title = es.text
    dict['url'] = url
    dict['title'] = title
    dics.append(dict)
    divs = html.xpath(pagexpath)
    prelog = 'https://ccst.jlu.edu.cn'
    for div in divs:
        rows = div.text[1:-1]

    pages = math.ceil(int(rows) / 10)
    curpages = pages

    while curpages != 0:
        content = []
        dict = {
            'url': [],
            'title': [],
            'content': [],
            'date': []
        }
        i = 1
        # 去取动态html转换为静态
        browser = webdriver.Edge(options=options)
        if curpages == pages:  # 说明当前在众多页中的第一页，则url不需要改变
            browser.get(url)
            curpages -= 1
        else:  # url需要改变
            url = url[:-4] + '/' + str(curpages) + url[-4:]
            curpages -= 1
            browser.get(url)

        htmlStr = browser.page_source
        browser.close()
        html = etree.HTML(htmlStr)  # 把静态字串转换为HTML

        # 下面开始获取li
        i = 1
        while i != 11:
            rowxpath = f'/html/body/div[3]/div[2]/div[2]/ul[1]/li[{i}]/a[1]'  # 获取连接用的xpath
            divs = html.xpath(rowxpath)  # 对HTML进行xpath解析（这一页包含很多li）
            for div in divs:
                content = []
                newUrl = prelog + '/' + div.get('href')
                # print(newUrl)
                # 下面对这个newUrl进行访问，并获取文章内容
                resp2 = requests.get(newUrl)
                resp2_headers = resp2.headers
                lastmodify = resp2_headers.get('Last-Modified')
                html2 = etree.HTML(resp2.content)
                titles = html2.xpath(titlexpath)
                for e in titles:
                    title = e.text  # 获取标题

                soup = BeautifulSoup(resp2.content, 'html.parser')

                # 找到id为vsb_content的div标签
                vsb_content_div = soup.find('div', id=['vsb_content', 'vsb_content_100'])

                # 获取该div内部的所有内容（包括标签）的字符串表示
                inner_content = str(vsb_content_div)
                inner_content = patternDrop.sub('', inner_content)
                subStrings = inner_content.split('</p>')

                for it in subStrings:
                    patternDrop.sub('', it)
                    patternStrong.sub('', it)
                    if it != '':
                        content.append(it)

                dict['url'] = newUrl
                dict['content'] = content
                dict['title'] = title
                dict['date'] = lastmodify
                dics.append(dict)
                print(dics)
            i += 1
    return dics
