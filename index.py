# -*- coding:utf-8 -*-
import werobot
from bottle import route,run

# weixin server
robot = werobot.WeRoBot(token='tabsunirumor', enable_session=True)
@robot.subscribe
def subscribe(message):
    return '欢迎关注iRumor！'

@robot.text
def articles(message):
    html_str =("""
        <html>
        <head>
            <title>YourMessage</title>
        </head>
        <body>
            <p>%s</p>
        </body>
        </html>""" % message.content)

    html_file= open("/var/vo/index.html","w")
    html_file.write(html_str)
    html_file.close()
    
    return [
        [
            "whtsky",
            "I wrote WeRobot",
            "https://secure.gravatar.com/avatar/0024710771815ef9b74881ab21ba4173?s=420",
            "http://tabsun-rumor-on-cloud-app.daoapp.io"
        ]
    ]

robot.run(host='0.0.0.0',port=80)
