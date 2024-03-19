from lxml import etree
import requests
import math
import re
from bs4 import BeautifulSoup
from selenium import webdriver


def work():
    url1 = 'https://ccst.jlu.edu.cn/syzx/gjjjsjsyjxsfzx/sfzxjj.htm'
    url2 = 'https://ccst.jlu.edu.cn/syzx/gjjjsjsyjxsfzx/jsjkxyjsfzx.htm'
    url3 = 'https://ccst.jlu.edu.cn/syzx/gjjjsjsyjxsfzx/jsjkxyjsfzx/dpjyqrssys.htm'
    url4 = 'https://ccst.jlu.edu.cn/syzx/gjjjsjsyjxsfzx/jsjkxyjsfzx/wjxtyjksys.htm'
    url5 = 'https://ccst.jlu.edu.cn/syzx/gjjjsjsyjxsfzx/jsjkxyjsfzx/wlyaqsys.htm'
    url6 = 'https://ccst.jlu.edu.cn/syzx/gjjjsjsyjxsfzx/jsjkxyjsfzx/jsjrjsys.htm'
    url7 = 'https://ccst.jlu.edu.cn/syzx/gjjjsjsyjxsfzx/jsjkxyjsfzx/wlwgczysys.htm'
    url8 = 'https://ccst.jlu.edu.cn/syzx/gjjjsjsyjxsfzx/jsjkxyjsfzx/kfcxsys.htm'
    url9 = 'https://ccst.jlu.edu.cn/syzx/gjjjsjsyjxsfzx/jsjkxyjsfzx/zxgg.htm'
    url10 = 'https://ccst.jlu.edu.cn/syzx/gjjwlwxnfzsyjxzx.htm'
    url11 = 'https://ccst.jlu.edu.cn/syzx/gjjjsjsyjxsfzx/syzxgzzd.htm'
    prelog = 'https://ccst.jlu.edu.cn'
    patternDrop = re.compile(r'<p[^>]*>|<\/p>|<br>|<br[^>]*>|&nbsp;|<span[^>]*>|'
                             r'<\/span>|<li[^>]*>|</li>|<ol[^>]*>|<\/ol>|'
                             r'<\/strong>|<ul[^>]*>|<\/ul>|<h1[^>]*>|</h1>|<td[^>]*>|</td>|'
                             r'<div[^>]*>|</div>|</form>|<h2[^>]*>|</h2>|<tbody>|<table>|<a[^>]*>|</a>|</tbody>|</table>|\n|\r|\u3000|\xa0')

    patternStrong = re.compile(r'<strong[^>]*>',re.S)

    urls = [url1, url2, url3, url4, url5, url6, url7, url8, url10]  # 只有九个url，因为url9比较特殊，需要单独爬取
    t = 0
    dics = []
    titlexpath = '/html/head/title[1]'
    while t != 10:
        dict = {
            'url': [],
            'title': [],
            'content': [],
            'date': []
        }
        content = []
        resp = requests.get(urls[t])
        resp_headers = resp.headers
        lastmodify = resp_headers.get('Last-Modified')
        html2 = etree.HTML(resp.content)
        titles = html2.xpath(titlexpath)
        for e in titles:
            title = e.text  # 获取标题
        soup = BeautifulSoup(resp.content, 'html.parser')
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
        dict['url'] = urls[t]
        dict['title'] = title
        dict['content'] = content
        dict['date'] = lastmodify
        dics.append(dict)
        print(dics)
        t += 1

    # 下面开始爬取url9和url11的内容
    urls2 = [url9,url11]
    t = 0
    while t != 2:
        dict = {
            'url': [],
            'title': [],
            'content': [],
            'date': []
        }
        content = []
        pagexpath = '/html/body/div[3]/div[2]/div[2]/div[1]/span[1]'
        resp = requests.get(urls2[t])
        html = etree.HTML(resp.content)
        titles = html.xpath(titlexpath)
        for es in titles:
            title = es.text
            
        dict['url'] = urls[t]
        dict['title'] = title
        dics.append(dict)
        
        coup = html.xpath(pagexpath)

        for it in coup:
            rows = int(it.text[1:4])

        pages = math.ceil(rows / 10)  # 以上pages计算出了一共有多少页
        curPage = pages
    
        while curPage != 0:
            browser = webdriver.Edge()
            if curPage == pages:  # 说明当前在众多页中的第一页，则url不需要改变
                browser.get(urls2[t])
                curPage -= 1
            else:  # url需要改变
                url = urls2[t][:-4] + '/' + str(curPage) + urls2[t][-4:]
                curPage -= 1
                browser.get(url)

            htmlStr = browser.page_source
            print(htmlStr)  # 将第t页的动态码转换为静态字串
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
                    resp = requests.get(newUrl)
                    resp_headers = resp.headers
                    lastmodify = resp_headers.get('Last-Modified')
                    soup = BeautifulSoup(resp.content, 'html.parser')
                    html2 = etree.HTML(resp.content)
                    titles = html2.xpath(titlexpath)
                    for e in titles:
                        title = e.text  # 获取标题
                    # 找到id为vsb_content的div标签
                    vsb_content_div = soup.find('div', id=['vsb_content','vsb_content_100'])

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
                    dict['title'] = title
                    dict['content'] = content
                    dict['date'] = lastmodify
                    dics.append(dict)
                    print(dics)

                i += 1
        t += 1
    return dics
