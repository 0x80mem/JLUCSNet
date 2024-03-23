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
    url1 = 'https://ccst.jlu.edu.cn/kxyj/xsdt.htm'
    url2 = 'https://ccst.jlu.edu.cn/kxyj/kytz.htm'
    url3 = 'https://ccst.jlu.edu.cn/kxyj/gjjl.htm'
    url4 = 'https://ccst.jlu.edu.cn/kxyj/zdsysjyjzx.htm'
    url5 = 'https://ccst.jlu.edu.cn/kxyj/yjs.htm'
    url6 = 'https://ccst.jlu.edu.cn/kxyj/zls.htm'

    urls = [url1, url2, url3, url5, url6]

    options = Options()
    options.use_chromium = True
    options.add_argument('--headless')
    prelog = 'https://ccst.jlu.edu.cn'
    i = 1

    t = 0

    patternDrop = re.compile(r'<p[^>]*>|<\/p>|<br>|<br[^>]*>|&nbsp;|<span[^>]*>|'
                             r'<\/span>|<li[^>]*>|</li>|<ol[^>]*>|<\/ol>|'
                             r'<\/strong>|<ul[^>]*>|<\/ul>|<h1[^>]*>|</h1>|<td[^>]*>|</td>|'
                             r'<div[^>]*>|</div>|</form>|<h2[^>]*>|</h2>|<tbody>|<table>|<a[^>]*>|</a>|</tbody>|</table>|\n|\r|\u3000|\xa0')

    patternStrong = re.compile(r'<strong[^>]*>', re.S)
    dics = []
    titlexpath = '/html/head/title[1]'
    while t != 5:
        dict = {
            'url': [],
            'title': [],
            'content': [],
            'date': []
        }
        pagexpath = '/html/body/div[3]/div[2]/div[2]/div[1]/span[1]'
        if findGotted(urls[t]) == -1:  # 说明此页面已经访问过，则不需要访问
            t += 1
            continue

        else:  # 该页面没访问过或者访问被中断
            resp = requests.get(urls[t])
            if resp.status_code == 200:
                addGotted(urls[t])
                html = etree.HTML(resp.content)
                titles = html.xpath(titlexpath)
                for es in titles:
                    title = es.text

                dict['url'] = urls[t]
                dict['title'] = title
                dics.append(dict)
                insertInfo(dict)
                coup = html.xpath(pagexpath)

                for it in coup:
                    rows = int(it.text[1:4])

                pages = math.ceil(rows / 10)  # 以上pages计算出了一共有多少页
                curPage = pages
                i = 1
                while curPage != 0:
                    browser = webdriver.Edge(options=options)
                    if curPage == pages:  # 说明当前在众多页中的第一页，则url不需要改变
                        browser.get(urls[t])
                        curPage -= 1
                        finUrl = urls[t]
                    else:  # url需要改变
                        url = urls[t][:-4] + '/' + str(curPage) + urls[t][-4:]
                        curPage -= 1
                        browser.get(url)
                        finUrl = url
                    htmlStr = browser.page_source
                    # print(htmlStr)#将第t页的动态码转换为静态字串
                    browser.close()
                    html = etree.HTML(htmlStr)  # 把静态字串转换为HTML

                    i = 1
                    while i != 11:
                        rowxpath = f'/html/body/div[3]/div[2]/div[2]/ul[1]/li[{i}]/a[1]'  # 获取连接用的xpath
                        divs = html.xpath(rowxpath)  # 对HTML进行xpath解析（这一页包含很多li）
                        for div in divs:
                            content = []
                            newUrl = prelog + div.get('href')[2:]
                            print(newUrl)
                            # 下面对这个newUrl进行访问，并获取文章内容
                            if findGotted(newUrl) == -1:  # 如果这个已经被访问过
                                continue
                            else:
                                resp = requests.get(newUrl)
                                if resp.status_code == 200:
                                    resp_headers = resp.headers  # 获取头部信息
                                    lastmodify = resp_headers.get('Last-Modified')  # 获取最后修改时间
                                    html2 = etree.HTML(resp.content)
                                    res = html2.xpath(titlexpath)
                                    for rs in res:
                                        title = rs.text
                                    soup = BeautifulSoup(resp.content, 'html.parser')

                                    # 找到id为vsb_content的div标签
                                    vsb_content_div = soup.find('div',id=['vsb_content', 'vsb_content_100', 'vsb_content_2'])

                                    # 获取该div内部的所有内容（包括标签）的字符串表示
                                    inner_content = str(vsb_content_div)
                                    inner_content = patternDrop.sub('', inner_content)
                                    '''if t == 1 or 3:
                                        subStrings = inner_content.split('<strong>')
                                    if t == 2:
                                        subStrings = inner_content.split('<br>')
                                    if t == 4:
                                        subStrings = inner_content.split('</p>')'''
                                    # 因为第三大页的格式相对不统一，因此就不进行划分

                                    inner_content = patternStrong.sub('', inner_content)
                                    if inner_content != '':
                                        content.append(inner_content)
                                    dict['url'] = newUrl
                                    dict['content'] = content
                                    dict['title'] = title
                                    dict['date'] = lastmodify
                                    dics.append(dict)
                                    insertInfo(dict)
                                    addGotted(newUrl)
                                    print(dict)
                                else:
                                    print("页面出错")

                        i += 1
                    addGotted(finUrl)
            else:
                print("页面出错")

        t += 1
    return dics


'''url1 = 'https://ccst.jlu.edu.cn/kxyj/xsdt.htm'
url2 = 'https://ccst.jlu.edu.cn/kxyj/kytz.htm'
url3 = 'https://ccst.jlu.edu.cn/kxyj/gjjl.htm'
url4 = 'https://ccst.jlu.edu.cn/kxyj/zdsysjyjzx.htm'
url5 = 'https://ccst.jlu.edu.cn/kxyj/yjs.htm'
url6 = 'https://ccst.jlu.edu.cn/kxyj/zls.htm'

urls = [url1,url2,url3,url4,url5,url6]
i = 0
prelog = 'https://ccst.jlu.edu.cn'
pagexpath = '/html/body/div[3]/div[2]/div[2]/div[1]/span[1]'
rowxpath = '/html/body/div[3]/div[2]/div[2]/UL[1]/li[1]/a[1]'
resp = requests.get(url1)
html = etree.HTML(resp.content)
coup = html.xpath(pagexpath)

for it in coup:
    rows = int(it.text[1:4])

pages =  math.ceil(rows/10)

t = 0
while t != 1:

    content = []
    resp = requests.get(urls[t])
    resp.encoding = 'UTF-8'
    html = etree.HTML(resp.content)

    i = 0
    while i != 10:
        divs = html.xpath(rowxpath)
        for div in divs:
            print("存在")
            newUrl = prelog + div.get('href')[2:]
            print(div.text)
        i += 1





    soup = BeautifulSoup(resp.content, 'html.parser')

    # 找到id为vsb_content的div标签
    vsb_content_div = soup.find('span', )

    # 获取该div内部的所有内容（包括标签）的字符串表示
    inner_content = str(vsb_content_div)

    inner_content = patternDrop.sub('',inner_content)

    subStrings = inner_content.split('<strong>')

    for it in subStrings:
        patternDrop.sub('',it)
        patternStrong.sub('',it)
        if it != '':
            content.append(it)

    key = urls[t]
    dic[key] = content
    t+=1'''
