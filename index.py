# -*- coding:utf-8 -*-
import werobot
import time
from string import Template

# weixin server
robot = werobot.WeRoBot(token='tabsunirumor', enable_session=True)
@robot.subscribe
def subscribe(message):
    return '欢迎关注iRumor！'

@robot.text
def articles(message):
    title_str = message.content
    date_str = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    title_str.encode('utf-8')
    #date_str.encode('utf-8')
    html_template ="""
        <html>
            <head>
            <title>$title</title>
            </head>

            <body>
            <h2>$title</h2>
            <hr />
            <p>$date tabsun iRumor</p>
            <br>
            <p>Just for test</p>
            <br>
            <p>更多内容关注iRumor</p>
            <img src="http://i.imgur.com/o8L9ItZ.jpg"/>
            </body>
        </html>"""
    html_template.substitute(title=title_str, date="2017-02-10")

    html_file= open("/var/ArticlePoolVolume/index.html","w")
    html_file.write(html_str)
    html_file.close()
    
    return [
        [
            "whtsky",
            "I wrote WeRobot",
            "https://secure.gravatar.com/avatar/0024710771815ef9b74881ab21ba4173?s=420",
            "http://tabsun-nginx-web.daoapp.io"
        ]
    ]

robot.run(host='0.0.0.0',port=80)
