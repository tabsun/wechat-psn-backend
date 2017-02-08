# -*- coding:utf-8 -*-
import werobot
from bottle import route

# weixin server
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

    #html_file= open("./index.html","w")
    #html_file.write(html_str)
    #html_file.close()
    
    return [
        [
            "whtsky",
            "I wrote WeRobot",
            "https://secure.gravatar.com/avatar/0024710771815ef9b74881ab21ba4173?s=420",
            "http://tabsun-rumor-on-cloud-app.daoapp.io/index.html"
        ]
    ]

#robot.run(host='0.0.0.0',port=80)


@route('/static/')
def static_content(filename):   
    current_folder = os.path.dirname(os.path.abspath(__file__))   
    static_file =   os.path.join(current_folder, '%s' % filename)   
    with open (static_file) as f:       
        content = f.read()       
    return content
bottle.run(host='0.0.0.0', port=8080)
