from lxml import etree
from PIL import Image
from io import BytesIO
from AItest import QianfanSemanticAnalysis
import requests
import re
from bs4 import BeautifulSoup
import pytesseract
import io


def work():
    urlMain = 'https://ccst.jlu.edu.cn/xkjs/zyyjfx1.htm'
    urlsoft = 'https://ccst.jlu.edu.cn/xkjs/zyyjfx1/jsjrjyll.htm'
    urlapp = 'https://ccst.jlu.edu.cn/xkjs/zyyjfx1/jsjyyjs.htm'
    urlsys = 'https://ccst.jlu.edu.cn/xkjs/zyyjfx1/jsjxtjg.htm'
    urlbio = 'https://ccst.jlu.edu.cn/xkjs/zyyjfx1/swxxx.htm'
    urlacadegree = 'https://ccst.jlu.edu.cn/xkjs/xwwyh1.htm'
    urlleadegree = 'https://ccst.jlu.edu.cn/xkjs/xswyh1.htm'
    urlteach = 'https://ccst.jlu.edu.cn/xkjs/jxwyh1.htm'
    urls = [urlMain,urlsoft,urlapp,urlsys,urlsys,urlbio,urlacadegree,urlleadegree,urlteach]

    patternDrop = re.compile(r'\xa0',re.S)

    dic = {}#用于存放url与每个url对应的内容，其中每个url对应的内容还要分段，为一个列表

    xpath = '/html/body/div[3]/div[2]/div[2]/div[1]/div[1]'

    patternDrop = re.compile(r'<p[^>]*>|<\/p>|<br>|<br[^>]*>|&nbsp;|<span[^>]*>|'
                             r'<\/span>|<li[^>]*>|</li>|<ol[^>]*>|<\/ol>|'
                             r'<\/strong>|<ul[^>]*>|<\/ul>|<h1[^>]*>|</h1>|<td[^>]*>|</td>|'
                             r'<div[^>]*>|</div>|</form>|<h2[^>]*>|</h2>|<tbody>|<table>|<a[^>]*>|</a>|</tbody>|</table>|\n|\r|\u3000|\xa0')

    patternStrong = re.compile(r'<strong[^>]*>',re.S)
    dics = []
    titlexpath = '/html/head/title[1]'
    t = 0
    while t != 9:
        dict = {
            'url': [],
            'title': [],
            'content': [],
            'date': []
        }
        content = []
        resp = requests.get(urls[t])
        html = etree.HTML(resp.content)
        divs = html.xpath(titlexpath)
        for div in divs:
            title = div.text
        resp_headers = resp.headers
        lastmodify = resp_headers.get('Last-Modified')
        resp.encoding = 'UTF-8'

        soup = BeautifulSoup(resp.content, 'html.parser')

        # 找到id为vsb_content的div标签
        vsb_content_div = soup.find('div', id='vsb_content')

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
        dict['url'] = urls[t]
        dict['title'] = title
        dict['content'] = content
        dict['date'] = lastmodify
        dics.append(dict)
        print(dics)
        t += 1
    return dics
