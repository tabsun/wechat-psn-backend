# -*- coding:utf-8 -*-
import time

def articles(message):
    title = message
    date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    html_str ="""
        <html>
            <head>
            <title>%s</title>
            </head>

            <body>
            <h2>%s</h2>
            <hr />
            <p>%s tabsun iRumor</p>
            <br>
            <p>Just for test</p>
            <br>
            <p>更多内容关注iRumor</p>
            <img src="http://i.imgur.com/o8L9ItZ.jpg"/>
            </body>
        </html>""" % (title, title, date)

    html_file= open("./show.html","w")
    html_file.write(html_str)
    html_file.close()

articles("qqq")
