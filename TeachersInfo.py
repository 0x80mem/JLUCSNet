from lxml import etree
from PIL import Image
from io import BytesIO
from AItest import QianfanSemanticAnalysis
from Config import cak
from Config import ocr
from Config import csk
import requests
import re
import pytesseract
import io
import OCRFunction


def work():
    url = "https://ccst.jlu.edu.cn/szdw/bssds.htm"
    urlPr = "https://ccst.jlu.edu.cn/szdw/js.htm"
    urlVicePr = "https://ccst.jlu.edu.cn/szdw/fjs.htm"
    urlTea = "https://ccst.jlu.edu.cn/szdw/js1.htm"
    urlReady = "https://ccst.jlu.edu.cn/szdw/zpzpjs.htm"
    urlZy = "https://ccst.jlu.edu.cn/__local/B/8E/7B/C1E6AB1D93EFB598D2A55ABD144_39E3C39D_144257.jpg?e=.jpg"
    urls = [url,urlPr,urlVicePr,urlTea,urlReady]
    pytesseract.pytesseract.tesseract_cmd = ocr
    newNames = []
    texts = []

    members = []
    dictionTea = {}


    def image2byte(image, photoFormat):
        img_bytes = io.BytesIO()
        image.save(img_bytes, format=photoFormat)
        image_bytes = img_bytes.getvalue()  # 这就是二进制数据
        return image_bytes


    def search(strTeacher):

        for key,value in members:
            if key == strTeacher:
                return value
            else:
                continue
        return '未找到相关信息！'

    prelog = 'https://ccst.jlu.edu.cn'
    #newUrl = 'https://ccst.jlu.edu.cn/info/1026/16992.htm'
    pattern = re.compile(r'<td[^>]*>(?P<want>.*?)</td>', re.S)
    #pattern2 = re.compile(r'/html/body/div[3]/div[2]/div[2]/div[1]/div[1]/p[1]',re.S)
    #pattern2 = re.compile(r'<p[^*]*>(?P<want>.*?)</p>',re.S)
    pattern2 = re.compile(r'<div class="article">.*?<p[^>]*>(?P<want2>.*)</p>.*?</div>', re.S)


    patternEmail = re.compile(r'Email：<img src="(?P<wantEmail>[^"]+)"',re.S)#尝试去匹配并提取图像的src
    patternTel = re.compile(r'电话：<img src="(?P<wantTel>[^"]+)"',re.S)#同理
    patternImg = re.compile(r'<img.*?src="(?P<wantPhoto>[^"]+)".*>.*?(Email|邮箱|电话)',re.S)#应该是以'姓名：'开头、并且Email结尾之间的唯一的那个img标签中的src才是人物照片
    #科研论文、代表性论文、部分论文、代表论文、论文成果、学术论文
    patternEassy = re.compile(r'(科研论文|代表性论文|部分论文|代表论文|论文成果|学术论文).*?(?P<wantEassy>.*)(工作经历|科研项目|出版教材|治学格言|著作教材|获奖情况)')
    i = 2
    t = 0
    patternDrop = re.compile(r'<p[^>]*>|<\/p>|<br>|<br[^>]*>|&nbsp;|<span[^>]*>|'
                             r'<\/span>|<li[^>]*>|</li>|<ol[^>]*>|<\/ol>|<strong[^>]*>|'
                             r'<\/strong>|<ul[^>]*>|<\/ul>|<h1[^>]*>|</h1>|'
                             r'<div[^>]*>|</div>|</form>|<h2[^>]*>|</h2>|<tbody>|<table>|<a[^>]*>|</a>|</tbody>|</table>')

    patternDropImage = re.compile(r'<img[^>].*?>',re.S)


    while t != 5:
        resp = requests.get(urls[t])
        resp.encoding = 'UTF-8'
        html = etree.HTML(resp.content)  # 可通用
        i = 2

        while i != 18:
            xpaths = [f'/html/body/div[3]/div[2]/div[2]/div[2]/p[{i}]/a',
                      f'/html/body/div[3]/div[2]/div[2]/div[1]/p[{i}]/a',
                      f'/html/body/div[3]/div[2]/div[2]/div[1]/p[{i}]/a',
                      f'/html/body/div[3]/div[2]/div[1]/p[{i}]/a',
                      f'/html/body/div[3]/div[2]/div[2]/ul[1]/li[{i}]/div[1]/div[2]/a[1]']

            divs = html.xpath(xpaths[t])

            for div in divs:
                print('姓名：',div.text,'链接：',prelog+div.get('href')[2:])
                newUrl = prelog+div.get('href')[2:]

                if div.text in newNames:
                    break

                newNames.append(div.text)
                resp2 = requests.get(newUrl)
                resp2.encoding = 'UTF-8'
                html2 = etree.HTML(resp2.content)
                texts = []
                try:
                    match = pattern.finditer(resp2.text)
                    test_empty = next(match)
                    for it in match:
                        '''final_text = it.group('want').replace('<p>', '')
                        final_text = final_text.replace('</p>', '')
                        final_text = final_text.replace('<br>', '')
                        final_text = final_text.replace('&nbsp', '')'''

                        final_text = patternDrop.sub('',it.group('want'))
                        #先找到是否有邮件（Email）和电话的相关信息
                        #laterMail = re.search(patternEmail,final_text)
                        texts.append(final_text)
                        '''try:
                            test_empty = next(laterMail)
                            Email = prelog + laterMail
                            print("Email为：",Email)
    
                        except StopIteration:
                            print("不存在邮箱图片")'''

                        #print(final_text)


                except StopIteration:
                    match2 = pattern2.finditer(resp2.text)
                    for it in match2:
                        final_text = patternDrop.sub('',it.group('want2'))
                        #laterMail = re.search(patternEmail,final_text)
                        texts.append(final_text)
                        #print(final_text)

                strLine = ''.join(texts)#把获得的一个老师的所有分条信息整合成一整条信息

                if 'Email' in strLine:#提取Email图像消息
                    Email = patternEmail.finditer(strLine)
                    for e in Email:
                        if e.group('wantEmail')[0] == '/':
                            EmailSource = prelog + e.group('wantEmail')
                            print(EmailSource)
                            response = requests.get(EmailSource)

                            if response.status_code == 200:
                                imageData = BytesIO(response.content)
                                image = Image.open(imageData)
                                #text = pytesseract.image_to_string(image)
                                text = OCRFunction.image2string(image)


                                strLine = strLine.replace("邮箱：","邮箱："+text).replace("Email：","Email："+text)

                                #print(text)
                                #strLine = patternDropImage.sub('Email：'+text,strLine)
                                #new_string = re.sub(r'((Email：|邮箱：)[\s\S]*?)<img.*?>', r'\1' + text, strLine)
                                #print('新字串：',new_string)
                                imageData.close()
                        else:
                            break

                else:
                    print("邮箱不为图片")
                if '电话：' in strLine:#提取图像电话信息
                    Telphone = patternTel.finditer(strLine)
                    for e in Telphone:
                        if e.group('wantTel')[0] == '/':
                            TelSource = prelog + e.group('wantTel')
                            print(TelSource)
                            response = requests.get(TelSource)
                            if response.status_code == 200:
                                imageData = BytesIO(response.content)
                                image = Image.open(imageData)
                                #text = pytesseract.image_to_string(image)
                                text = OCRFunction.image2string(image)
                                strLine = strLine.replace("电话：","电话："+text)


                                #strLine = patternDropImage2.sub('电话：'+text,strLine)
                                #new_string = re.sub(r'(电话：[\s\S]*?)<img.*?>', '电话：'+ text, strLine)
                                imageData.close()
                        else:
                            break

                else:
                    print("电话不为图片")
                if 'Email：' or '邮箱：' in strLine:
                    print('进入if')
                    photo = patternImg.finditer(strLine)
                    for p in photo:
                        print('进入for')
                        if p.group('wantPhoto')[0] == '/' and '教书育人是我的工作'not in strLine:
                            print('进入二层if')
                            photoSource = prelog + p.group('wantPhoto')
                            print(photoSource)
                            response = requests.get(photoSource)#打开图片
                            if response.status_code == 200:
                                #先获取图片的格式，因为有可能是jpeg，有可能是jpg，有可能是png
                                if photoSource[-2] == 'e':#说明是jpeg格式
                                    photoFormat = 'JPEG'
                                if photoSource[-2] == 'p':
                                    photoFormat = 'JPEG'
                                if photoSource[-2] == 'n':
                                    photoFormat = 'PNG'

                                try:
                                    imageData = BytesIO(response.content)
                                    image = Image.open(imageData)
                                    image_bytes = image2byte(image,photoFormat.upper())
                                    #print('图片的二进制数据为：',image_bytes)

                                except IOError:
                                    print("图片无法打开！")
                        if '教书育人是我的工作' in strLine:
                            response = requests.get(urlZy)
                            photoFormat = 'JPEG'
                            print(urlZy)
                            try:
                                imageData = BytesIO(response.content)
                                image = Image.open(imageData)
                                image_bytes = image2byte(image,photoFormat.upper())
                                #print('图片的二进制数据为：',image_bytes)

                            except IOError:
                                print('图片无法打开')

                else:
                    print("不存在照片")
                #dictionTea[div.text] = strLine
                strLine = patternDropImage.sub('',strLine)
                memberInfo = strLine#+image_bytes
                print(memberInfo)
                members.append((div.text,memberInfo))
            i += 1
        t += 1



    #print(strs)
    # 替换成您的 API Key 和 Secret Key
    ak = cak
    sk = csk

    qianfan_sa = QianfanSemanticAnalysis(ak, sk)
    precommand = ("对提供的文段进行语义分析，提取出如下信息："
                  "（姓名，性别，邮箱，联系电话，最高学历，最高学位，办公地址，教研室，学科专业，研究方向，讲授课程，教育经历，工作经历，科研项目，学术论文，著作教材，获奖情况，社会兼职，科研成果，学生培养，治学格言，职称名称，毕业院校，个人简介，访问经历，荣誉奖励，报告交流，学术服务），"
                  "如果有文字与以上任意一条均不匹配，则将其归为（其他），如果有条目可以与多项匹配，则将其归为最为接近的一项，"
                  "如果有一项没有任何信息与之匹配，则该项以‘无’填充即可，并且提取的信息严格按照'姓名'：'xx'的格式，不要多加任何字符")
        # 输入要进行语义分析的文本
    input_text = input("请输入要搜索的教师姓名：")
    strs = search(input_text)
        # 获取语义分析结果
    result = qianfan_sa.semantic_analysis(precommand + strs)

        # 输出语义分析结果
    print("语义分析结果：", result)
    return members
