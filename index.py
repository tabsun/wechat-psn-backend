# -*- coding:utf-8 -*-
import werobot
import time
from string import Template

# weixin server
robot = werobot.WeRoBot(token='tabsunirumor', enable_session=True)
@robot.subscribe
def subscribe(message):
    return '欢迎关注irumor！'

@robot.text
def articles(message):
    title_str = message.content
    date_str = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    title_str = title_str.encode('utf-8')
    #date_str.encode('utf-8')
    html_str1 ="""
        <html>
            <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            <title>irumor</title>
            </head>

            <body>
            <h2>"""
    html_str2 = """</h2>
            <hr />
            <p>"""
    html_str3 = """ tabsun irumor</p>
            <br>
            <p>Just for test</p>
            <br>
            <p>更多内容关注irumor</p>
            <img src="http://i.imgur.com/o8L9ItZ.jpg"/>
            </body>
        </html>"""
    html_str = html_str1 + title_str + html_str2 + date_str + html_str3

    html_file= open("/var/ArticlePoolVolume/index.html","w")
    html_file.write(html_str)
    html_file.close()
    
    return [
        [
            "whtsky",
            "I wrote WeRobot",
            "http://img0.imgtn.bdimg.com/it/u=3324759509,3214419485&fm=23&gp=0.jpg",
            "http://tabsun-nginx-web.daoapp.io"
        ]
    ]

robot.run(host='0.0.0.0',port=80)
