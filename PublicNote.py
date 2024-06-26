from lxml import etree
import requests
import math
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from checkUrl import addGotted
from checkUrl import findGotted
def work(insertInfo):
    url1 = 'https://ccst.jlu.edu.cn/xwzx/xytz.htm'
    url2 = 'https://ccst.jlu.edu.cn/xwzx/xyxw.htm'
    url3 = 'https://ccst.jlu.edu.cn/xwzx/xstd.htm'
    url4 = 'https://ccst.jlu.edu.cn/xwzx/zsjy.htm'
    url5 = 'https://ccst.jlu.edu.cn/xwzx/gsl.htm'

    urls = [url1, url2, url3, url4, url5]
    options = Options()
    options.use_chromium = True
    options.add_argument('--headless')
    prelog = 'https://ccst.jlu.edu.cn'
    patternDrop = re.compile(r'<p[^>]*>|<\/p>|<br>|<br[^>]*>|&nbsp;|<span[^>]*>|'
                             r'<\/span>|<li[^>]*>|</li>|<ol[^>]*>|<\/ol>|'
                             r'<\/strong>|<ul[^>]*>|<\/ul>|<h1[^>]*>|</h1>|<td[^>]*>|</td>|'
                             r'<div[^>]*>|</div>|</form>|<h2[^>]*>|</h2>|<tbody>|<table>|<a[^>]*>|</a>|</tbody>|</table>|\n|\r|\u3000|\xa0')

    patternStrong = re.compile(r'<strong[^>]*>', re.S)

    dics = []
    titlexpath = '/html/head/title[1]'

    t = 0
    while t != 5:
        content = []
        dict = {
            'url': [],
            'title': [],
            'content': [],
            'date': [],
            'realtime':''
        }
        pagexpath = '/html/body/div[3]/div[2]/div[2]/div[1]/span[1]'
        if findGotted(urls[t]) == -1:
            t += 1
            continue
        else:
            resp = requests.get(urls[t])
            if resp.status_code == 200:
                html = etree.HTML(resp.content)
                titles = html.xpath(titlexpath)
                for es in titles:
                    title = es.text

                dict['title'] = title
                dict['url'] = urls[t]
                insertInfo(dict)
                dics.append(dict)

                divs = html.xpath(pagexpath)
                for div in divs:
                    rows = div.text[1:-1]

                pages = math.ceil(int(rows) / 10)
                curpages = pages

                # 先获取页面的动态html，将其转化为静态代码
                while curpages != 0:
                    i = 1
                    browser = webdriver.Edge(options=options)
                    if curpages == pages:  # 说明当前在众多页中的第一页，则url不需要改变
                        browser.get(urls[t])
                        curpages -= 1
                        finUrl = urls[t]
                    else:  # url需要改变
                        url = urls[t][:-4] + '/' + str(curpages) + urls[t][-4:]
                        curpages -= 1
                        browser.get(url)
                        finUrl = url
                    htmlStr = browser.page_source
                    # print(htmlStr)  # 将第t页的动态码转换为静态字串
                    browser.close()
                    html = etree.HTML(htmlStr)  # 把静态字串转换为HTML

                    # 下面开始获取li
                    i = 1
                    while i != 11:
                        rowxpath = f'/html/body/div[3]/div[2]/div[2]/ul[1]/li[{i}]/a[1]'  # 获取连接用的xpath
                        rowdatexpath = f'/html/body/div[3]/div[2]/div[2]/ul[1]/li[{i}]/span[1]'  # 用于获取真正的时间
                        timeDivs = html.xpath(rowdatexpath)
                        for timeDiv in timeDivs:
                            realTime = timeDiv.text
                            dict['realtime'] = realTime
                        divs = html.xpath(rowxpath)  # 对HTML进行xpath解析（这一页包含很多li）
                        for div in divs:
                            content = []
                            newUrl = prelog + div.get('href')[2:]
                            # print(newUrl)
                            # 下面对这个newUrl进行访问，并获取文章内容
                            if findGotted(newUrl) == -1:
                                t += 1
                                continue
                            else:
                                resp2 = requests.get(newUrl)
                                if resp2.status_code == 200:
                                    resp2_headers = resp2.headers
                                    lastmodify = resp2_headers.get('Last-Modified')
                                    html2 = etree.HTML(resp2.content)
                                    titles = html2.xpath(titlexpath)
                                    for e in titles:
                                        title = e.text  # 获取标题

                                    soup = BeautifulSoup(resp2.content, 'html.parser')

                                    # 找到id为vsb_content的div标签
                                    vsb_content_div = soup.find('div', id=['vsb_content', 'vsb_content_100','vsb_content_2'])

                                    # 获取该div内部的所有内容（包括标签）的字符串表示
                                    inner_content = str(vsb_content_div)
                                    inner_content = patternDrop.sub('', inner_content)
                                    inner_content = patternStrong.sub('', inner_content)
                                    if inner_content != '':
                                        content.append(inner_content)

                                    dict['url'] = newUrl
                                    dict['content'] = content
                                    dict['title'] = title
                                    dict['date'] = lastmodify
                                    insertInfo(dict)
                                    addGotted(newUrl)
                                    dics.append(dict)
                                    print(dict)
                                else:
                                    print("页面出错")
                        i += 1
                    addGotted(finUrl)
                t += 1
            else:
                print("页面出错")
                t += 1
    return dics
