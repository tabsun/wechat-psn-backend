# -*- coding:utf-8 -*-
import werobot

#robot = werobot.WeRoBot(token='robot', enable_session=True, session_storage=saekvstorage.SaeKVDBStorage())
#robot = werobot.WeRoBot(token='testrobot', enable_session=True, session_storage=filestorage.FileStorage())
robot = werobot.WeRoBot(token='tabsunirumor', enable_session=True)

@robot.subscribe
def subscribe(message):
    return '欢迎关注iRumor！'

@robot.text
def articles(message):
    html_str = """
        <html>
        <head>
            <title>test</title>
        </head>
        <body>
            <p>body of test</p>
        </body>
        </html>
        """

    html_file= open("./index.html","w")
    html_file.write(html_str)
    html_file.close()
    
    return [
        [
            "whtsky",
            "I wrote WeRobot",
            "https://secure.gravatar.com/avatar/0024710771815ef9b74881ab21ba4173?s=420",
            "http://tabsun-rumor-on-cloud-app.daoapp.io/article.html"
        ]
    ]

robot.run(host='0.0.0.0',port=80)
