from lxml import etree
from PIL import Image
from io import BytesIO
from AItest import QianfanSemanticAnalysis
from Config import ocr
import requests
import re
import pytesseract
import io
import OCRFunction
from histroy import History
def work():
    urlIntro = "https://ccst.jlu.edu.cn/xygk/xyjj.htm"
    urlMessage = "https://ccst.jlu.edu.cn/xygk/yzjy.htm"
    #urlLeader = "https://ccst.jlu.edu.cn/xygk/xrld.htm"
    urlHis = "https://ccst.jlu.edu.cn/xygk/lsyg.htm"
    urls = [urlIntro,urlMessage,urlHis]
    pytesseract.pytesseract.tesseract_cmd = ocr
    patternDrop = re.compile(r'\xa0',re.S)
    patternImg = re.compile(r'<p style="text-align: left;">.*?<img.*?src="(?P<wantPhoto>[^"]+)".*?>',re.S)
    dic = {}#用于存放url与每个url对应的内容，其中每个url对应的内容还要分段，为一个列表

    xpaths = ['/html/body/div[3]/div[2]/div[2]/div[1]/div[1]/div[1]/p',
              '/html/body/div[3]/div[2]/div[2]/div[1]/div[1]/div[1]/p',
              '/html/body/div[3]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/p']#每个页面用于定位的xpath
    prelog = 'https://ccst.jlu.edu.cn'
    dics = []
    titlexpath = '/html/head/title[1]'
    t = 0
    while t != 3:
        dict = {
            'url': [],
            'title': [],
            'content': [],
            'date': []
        }
        content = []
        resp = requests.get(urls[t])
        if resp.status_code == 200:
            resp_headers = resp.headers
            lastmodify = resp_headers.get('Last-Modified')
            resp.encoding = 'UTF-8'
            html = etree.HTML(resp.content)
            titles = html.xpath(titlexpath)
            for rs in titles:
                title = rs.text

            divs = html.xpath(xpaths[t])
            for div in divs:
                #下面将对p标签的内容进行读取，并且每个p标签均存到数组中
                if div.text!=None:
                    div.text = patternDrop.sub('', div.text)
                    if div.text != '':
                        content.append(div.text)
                if t == 2:
                    content.append(History())
                    '''match = patternImg.finditer(resp.text)

                    for it in match:

                        if it.group('wantPhoto'):
                            source = prelog + it.group('wantPhoto')
                            response = requests.get(source)
                            if response.status_code == 200:
                                imageData = BytesIO(response.content)
                                image = Image.open(imageData)
                                #text = pytesseract.image_to_string(image)
                                text = OCRFunction.image2string(image)
                                content.append(text)
                                imageData.close()
                        else:
                            break'''
            key = urls[t]
            dict['url'] = urls[t]
            dict['title'] = title
            dict['content'] = content
            dict['date'] = lastmodify
            dics.append(dict)
            print(dict)
            t += 1

        else:
            print("页面不存在")
            t += 1

    return dics

