from lxml import etree
import requests
import math
import re
from bs4 import BeautifulSoup
from selenium import webdriver

url1 = 'https://ccst.jlu.edu.cn/rcpy/bksjy/jxtz.htm'
url2 = 'https://ccst.jlu.edu.cn/rcpy/bksjy/zyjs.htm'
url3 = 'https://ccst.jlu.edu.cn/rcpy/bksjy/kcjj.htm'
url4 = 'https://ccst.jlu.edu.cn/rcpy/bksjy/sxsxw.htm'
urls = [url1,url2,url3,url4]


prelog = 'https://ccst.jlu.edu.cn'
i = 1

t = 0

patternDrop = re.compile(r'<p[^>]*>|<\/p>|<br>|<br[^>]*>|&nbsp;|<span[^>]*>|'
                         r'<\/span>|<li[^>]*>|</li>|<ol[^>]*>|<\/ol>|'
                         r'<\/strong>|<ul[^>]*>|<\/ul>|<h1[^>]*>|</h1>|<td[^>]*>|</td>|'
                         r'<div[^>]*>|</div>|</form>|<h2[^>]*>|</h2>|<tbody>|<table>|<a[^>]*>|</a>|</tbody>|</table>|\n|\r|\u3000|\xa0')

patternStrong = re.compile(r'<strong[^>]*>',re.S)
dics = []
titlexpath = '/html/head/title[1]'
while t != 2:
    dict = {
        'url': [],
        'title': [],
        'content': [],
        'date': []
    }
    pagexpath = '/html/body/div[3]/div[2]/div[2]/div[1]/span[1]'
    resp = requests.get(urls[t])
    html = etree.HTML(resp.content)
    coup = html.xpath(pagexpath)

    for it in coup:
        rows = int(it.text[1:4])

    pages = math.ceil(rows / 10)  # 以上pages计算出了一共有多少页
    curPage = pages
    i = 1
    while curPage !=0:
        browser = webdriver.Edge()
        if curPage == pages:#说明当前在众多页中的第一页，则url不需要改变
            browser.get(urls[t])
            curPage -=1
        else:#url需要改变
            url = urls[t][:-4] + '/'+str(curPage) + urls[t][-4:]
            curPage -= 1
            browser.get(url)

        htmlStr = browser.page_source
        print(htmlStr)#将第t页的动态码转换为静态字串
        browser.close()
        html = etree.HTML(htmlStr)#把静态字串转换为HTML

        i = 1
        while i != 11:
            rowxpath = f'/html/body/div[3]/div[2]/div[2]/ul[1]/li[{i}]/a[1]'  # 获取连接用的xpath
            divs = html.xpath(rowxpath)  # 对HTML进行xpath解析（这一页包含很多li）
            for div in divs:
                content = []
                newUrl = prelog + div.get('href')[2:]
                print(newUrl)
                #下面对这个newUrl进行访问，并获取文章内容
                resp2 = requests.get(newUrl)
                resp2_headers = resp2.headers
                lastmodify = resp2_headers.get('Last-Modified')

                html2 = etree.HTML(resp2.content)
                titles = html2.xpath(titlexpath)
                for e in titles:
                    title = e.text  # 获取标题
                soup = BeautifulSoup(resp2.content, 'html.parser')

                # 找到id为vsb_content的div标签
                vsb_content_div = soup.find('div', id='vsb_content')

                # 获取该div内部的所有内容（包括标签）的字符串表示
                inner_content = str(vsb_content_div)
                inner_content = patternDrop.sub('', inner_content)
                subStrings = inner_content.split('</p>')
                #因为第三大页的格式相对不统一，因此就不进行划分


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

    t +=1

content = []
r = 1

tdXpath = './a'
resp = requests.get(url3)
html = etree.HTML(resp.content)
while r !=27:
    dict = {
        'url': [],
        'title': [],
        'content': [],
        'date': []
    }
    tableXpath = f'/html/body/div[3]/div[2]/div[4]/table[1]/tbody[1]/tr[{r}]/td'
    divs = html.xpath(tableXpath)

    for div in divs:
        nextdiv = div.xpath(tdXpath)#二次xpath，去找a标签
        for it in nextdiv:
            NewUrl = prelog + it.get('href')[2:]  # 这样就获得了一门课程的url连接
            print(NewUrl)
            #下面可以进入到连接中爬取数据
            resp = requests.get(NewUrl)
            resp_headers = resp.headers
            lastmodify = resp_headers.get('Last-Modified')
            html2 = etree.HTML(resp.content)
            titles = html2.xpath(titlexpath)
            for e in titles:
                title = e.text  # 获取标题
            soup = BeautifulSoup(resp.content,'html.parser')
            vsb_content_div = soup.find('div', id='vsb_content')

            # 获取该div内部的所有内容（包括标签）的字符串表示
            inner_content = str(vsb_content_div)
            inner_content = patternDrop.sub('', inner_content)
            subStrings = inner_content.split('</p>')

            for it2 in subStrings:
                patternDrop.sub('', it2)
                patternStrong.sub('', it2)
                if it2 != '':
                    content.append(it2)
            dict['url'] = newUrl
            dict['title'] = title
            dict['content'] = content
            dict['date'] = lastmodify
            dics.append(dict)
            print(dics)
    r += 1


'''#下面爬取人才培养中“研究生教育”这一部分的内容
url1 = 'https://ccst.jlu.edu.cn/rcpy/yjsjy/yjszs.htm'
url2 = 'https://ccst.jlu.edu.cn/rcpy/yjsjy/yjspy.htm'
url3 = 'https://ccst.jlu.edu.cn/rcpy/yjsjy/xwsy.htm'
url4 = 'https://ccst.jlu.edu.cn/rcpy/yjsjy/bshgz.htm'
url5 = 'https://ccst.jlu.edu.cn/rcpy/yjsjy/yjsdj.htm'
url6 = 'https://ccst.jlu.edu.cn/rcpy/yjsjy/sxzzjy.htm'
url7 = 'https://ccst.jlu.edu.cn/rcpy/yjsjy/yjsgl.htm'
url8 = 'https://ccst.jlu.edu.cn/rcpy/yjsjy/sjyjy.htm'
url9 = 'https://ccst.jlu.edu.cn/rcpy/yjsjy/yjszzyhd.htm'

urls = [url1,url2,url3,url4,url5,url6,url7,url8,url8]
t = 2
while t != 9:
    pagexpath = '/html/body/div[3]/div[2]/div[2]/div[1]/span[1]'
    resp = requests.get(urls[t])
    html = etree.HTML(resp.content)
    coup = html.xpath(pagexpath)

    for it in coup:
        rows = int(it.text[1:4])

    pages = math.ceil(rows / 10)  # 以上pages计算出了一共有多少页
    curPage = pages'''

