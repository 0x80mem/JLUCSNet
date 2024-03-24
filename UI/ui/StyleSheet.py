# 主窗口
mainWindow = \
    '''
    MainWindow{
        background-color:rgb(33,33,33);
        border: 2px solid rgb(50,50,50);
    } 
    '''
# 标题栏
head_widget = \
    '''
    QWidget { 
        background-color: rgb(50,50,50); 
        border-left: 2px solid rgb(50,50,50);
        border-right: 2px solid rgb(50,50,50);
    }
    '''
# 标题栏按钮widget
head_btn_widget = \
    '''
    QPushButton {
       width: 40px;
       height: 40px;
       border: none;
       border-radius:10px;
    }
    '''
# 退出按钮
exitBtn = \
    '''
    QPushButton{
        border-image:url(./img/close1.png);
    }
    QPushButton::hover{
        border-image:url(./img/close2.png);
    }
   
    '''
# 最小化按钮
minBtn = \
    '''
    QPushButton{
        border-image:url(./img/minus1.png);
    }
    QPushButton::hover{
        border-image:url(./img/minus2.png);
    }
    '''
# 还原/最大化按钮
restore_btn = \
    '''
    QPushButton{
        border-image:url(./img/restore1.png);
    }
    QPushButton::hover{
        border-image:url(./img/restore2.png);
    }
    
    '''
# 显示窗口
chat_widget = \
    '''
    QWidget#chat_widget{
        background-color:rgb(33,33,33);
        border-right: 2px solid rgb(50,50,50);
        border-left: 2px solid rgb(50,50,50);
    }
    '''
# 滚动区域滚动条样式
chat_area_verticalScrollBar = \
    '''
    QScrollBar:vertical {
        background: rgb(50,50,50);
        width: 15px;  
        border-right: 2px solid rgb(50,50,50)
    }
    QScrollBar::handle:vertical {
        background: transparent; 
        min-height: 20px;  
    }
    QScrollBar::add-line:vertical {
        height: 0px;  
    
    }
    QScrollBar::sub-line:vertical {
        height: 0px;  
    
    }
    QScrollBar::sub-page:vertical {
        background: rgb(33,33,33);
    
    }
    QScrollBar::add-page:vertical {
        background: rgb(33,33,33);
    
    }
    QScrollBar::handle::hover:vertical {
        background: rgb(66,66,66);
    
    }
    '''
# 发送按钮
send_button = \
    '''
    QPushButton {
        outline: 1px solid #0000ff;
        background-color: rgb(48, 48, 48);
        color: rgb(158, 158, 158);
        border-radius:20px;
        padding: 2px;
        margin-bottom:20px;
    }
    QPushButton:hover{
        outline: 1px solid #0000ff;
        background-color: rgb(180, 180, 180);
        color: rgb(0, 0, 0);
        border-radius:20px;
        padding: 2px;
        margin-bottom:20px;
    }
    '''
# 输入框
input_edit = \
    '''
    QTextEdit#inputEdit{
        font-family:微软雅黑;
        letter-spacing:3px;
        color:rgb(200, 200,200);
        font-size:25px;
        padding-left:20px;
        padding-right:110px;
        padding-top:10px;
        margin-bottom:20px;
        border-radius:30px;
        background-color:rgb(33, 33, 33);
        border: 2px solid rgb(100, 100, 100);
    }
    '''
# UserMsgBrowser
UserMsgBrowser = \
    '''
    QTextBrowser{
        background-color:rgb(33, 33, 33);
        margin-left:80px
    }      
    '''
UserMsgBrowser_html_p = \
    '''
    <p style='
        font-family:微软雅黑;
        font:27px;
        color:rgb(240, 240, 240);
        line-height:20px;
        width:100% ; white-space:
        pre-wrap; letter-spacing: 3px
    '>  
    '''
# AIMsgBrowser
AIMsgBrowser = \
    '''
    QTextBrowser{
        background-color:rgb(33, 33, 33);
        margin-left:80px;
        color:rgb(240, 240, 240);
    }
    '''
AIMsgBrowser_html = \
    '''
    <!DOCTYPE html>
        <html>
        <head>
            <title>HTML Table Example</title>
            <style>
                a:link{
                    color: rgb(50, 200, 50);
                }

                table {
                    margin: 10px 10px;
                    border-collapse: collapse;
                }
                        
                th, td {
                    border: 1px solid black;
                    padding: 10px;
                    text-align: left;
                    color:black;
                }
                th {
                    background-color: rgb(20,20,20);
                    color: rgb(200,200,200);
                    font-size: 25px;
                    white-space: pre-line;
                    padding: 20px;
                    font-family: 华文中宋;
                }
                p{
                    font-family:微软雅黑;
                    font:27px;
                    color:rgb(240, 240, 240);
                    line-height:1.5;
                    width:100% ; 
                    white-space:pre-wrap; 
                    letter-spacing: 3px;
                    margin-bottom:10px;
                }
                code{
                    color:rgb(46,178,202);
                    background-color: black;
                }
            </style>
        </head>
        <body>
    '''
# SystemMsgBrowser
SystemMsgBrowser = \
    '''
    QTextBrowser{
        background-color:rgb(55, 55, 55);
        margin-left:80px;
        color:rgb(240, 240, 240);
        border-radius:10px;
        padding:10px;
    }
    '''
SystemMsgBrowser_html_p = \
    '''
    <p style='
        font-family: Arial, Helvetica, sans-serif;
        font:27px;
        color:rgb(255, 80,80);
        line-height:20px;
        width:100% ; 
        white-space:pre-wrap; 
        letter-spacing: 3px
    '>
    '''
# DataBaseMsgBrowser
DataBaseMsgBrowser = \
    '''
    QTextEdit{
        background-color:rgb(33, 33, 33);
        margin-left:80px;
        color:rgb(240, 240, 240);
        border-radius:10px;
        padding:10px;
    }    
    '''
DataBaseMsgBrowser_html = \
    '''
   <!DOCTYPE html>
    <html>
    <head>
        <title>Student Information Table</title>
        <style>
            a{
                color: rgb(100, 100, 240);
            }
            table {
                margin: 10px 10px;
                border-collapse: collapse;
                
            }
            th, td {
                border: 1px solid rgb(100,100,100);
                
                padding: 8px;
                text-align: left;
            }            
            #doc{
                background-color: rgb(100,100,100);
                color: #5ad1e6;
                font-style: italic;
                font-size: 20px;
                font-family: 幼圆; /* 设置字体为 Arial 或者系统默认 sans-serif 字体 */
                
            }
            #title{
                text-align: center; /* 水平居中 */
                height: 50px;
                line-height: 50px;
                border-bottom: 0;
                border-top: 0;
                font-family: 华文中宋;
                font-size:40px;
            }
            #content{
                border-top: 0;
                border-bottom: 0;
                padding-left: 20px; /* 左边距为 10px */
                padding-right: 20px; /* 右边距为 10px */
                word-wrap: break-word;
                white-space: pre-wrap;
                font-size:30px;
                font-family:华文仿宋;
            }
            #url{
                text-align: right;
                border-top: 0;
                border-bottom: 0;
                font-size:30px;
            }
            #date{
                text-align: right; /* 文本靠右对齐 */
                border-top: 0;
                font-size:25px;
            }
            #comp_ratio{
                font-size:20px;
            }
        </style>
    </head>
    <body>          
    '''