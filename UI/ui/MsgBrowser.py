import markdown2
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QTextBrowser
import ui.StyleSheet as qss


class UserMsgBrowser(QTextBrowser):
    def __init__(self, parent):
        super().__init__()
        self.setParent(parent)
        self.setStyleSheet(qss.UserMsgBrowser)
        self.setAttribute(Qt.WA_StyledBackground, True)

    def setText(self, text):
        text = qss.UserMsgBrowser_html_p + text + "</p>"
        super().setText(text)


class AIMsgBrowser(QTextBrowser):
    def __init__(self, parent):
        super().__init__()
        self.setParent(parent)
        self.setStyleSheet(qss.AIMsgBrowser)

    def setText(self, text):
        html = qss.AIMsgBrowser_html

        md = markdown2.markdown(text, extras=["fenced-code-blocks"])

        md = md.replace("<pre><code>", """</p><table><tr><th width=100%>""")
        md = md.replace("</code></pre>", "</th></tr></table>")
        html_text = html + md + \
            """
                </body>
                </html>
            """
        self.setHtml(html_text)


class SystemMsgBrowser(QTextBrowser):
    def __init__(self, parent):
        super().__init__()
        self.setParent(parent)
        self.setStyleSheet(qss.SystemMsgBrowser)

    def setText(self, text):
        text = qss.SystemMsgBrowser_html_p + text + "</p>"

        super().setText(text)


class DataBaseMsgBrowser(QTextBrowser):
    def __init__(self, parent):
        super().__init__()
        self.setParent(parent)
        self.setOpenLinks(False)
        self.setStyleSheet(qss.DataBaseMsgBrowser)
        self.anchorClicked.connect(self.on_anchorClicked)

    def on_anchorClicked(self, url):
        # 在默认浏览器中打开链接
        QDesktopServices.openUrl(url)

    def setText(self, data_list):
        # # 开启测试文档
        # from ui.TestDocument import Database_test_list
        # data_list = Database_test_list
        
        html = qss.DataBaseMsgBrowser_html
        '''
                    -list
                        -tuple
                            -document
                                -page_content(str)
                                -meta_data(dic)
                                    -'url':str
                                    -'title':str
                                    -'date': str or empty list
                            -float

        '''
        for data_tuple in data_list:
            # 拆解数据
            doc = data_tuple[0]
            meta_data = doc.metadata
            doc_data = {
                'title': meta_data.get('title') if meta_data.get('title') is not None else '',
                'content': doc.page_content,
                'url': meta_data.get('url') if meta_data.get('url') is not None else '',
                'date': '时间：' + meta_data.get('date') if meta_data.get('date') is not None and type(meta_data.get('date')) == str else '',
                'comp_ratio': '文本差异度：' + str(data_tuple[1].item())
            }
            if doc_data.get('url') is not None:
                doc_data['url'] = '''<a href="''' + doc_data['url'] + '''">''' + doc_data['url'] + '''</a>'''
            # 单篇背景资料html
            tuple_html = '''
                 <tr>
                    <th id="doc">背景资料</th>
                </tr>
            '''
            # 添加title
            for key in doc_data:
                tuple_html += '''
                    <tr>
                    <th width=100% id="''' + key + '''">''' + doc_data[key] + '''</th>
                    </tr>
                '''
            html = html + tuple_html + ' </table> <br><br><br>'

        html += """
                </body>
            </html>
            """

        self.setHtml(html)
