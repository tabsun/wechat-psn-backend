# -*- coding:utf-8 -*-
import werobot
import time
from string import Template
from BaiduImageSearch import BaiduImage
import hashlib
import os

def GetFileMd5(filename):
    if not os.path.isfile(filename):
        return None
    myhash = hashlib.md5()
    f = file(filename,'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()

# weixin server
robot = werobot.WeRoBot(token='tabsunirumor', enable_session=True)
@robot.subscribe
def subscribe(message):
    return '欢迎关注irumor！'

@robot.text
def articles(message):
    opinion_str = message.content  
    opinion_str = opinion_str.encode('utf-8')
    date_str = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    # get article's title and content about the opinion
    title_str = opinion_str
    content_str = """《奇葩说》第二季里有一个辩题是：女生该不该追男生？\n
        喵以为，这个辩题的要点在“怎么定义追”？如果采取大众定义，“追=表白+付出的行为”。
        那么，在中国的语境下，我的答案是：不该！除非三个条件……\n
        不过，喵喵君提供一个心理学精神分析学派的视角来看这个问题。逻辑链条有点长，
        请智商100+的同学们慢慢follow，这还要从重男轻女的社会说起！\n\n
        【重男轻女社会的悲剧轮回】\n
        （地图炮预警！不过主要是对这三个省的情况比较熟悉，不代表这些省份的所有人都这样，
        也不代表其他省份就不这样）\n
        众所周知，中国（尤其大汉族沙文主义兴盛的东南三省），重男轻女仍十分严重（
        闽赣和粤之潮汕地区三省的女孩子，向你们投去深深的同情，据我所知，这部分地区
        依然男女分桌，不生男孩的女人会没地位，好强的女人会逼自己的孩子跟自己姓来传宗接代）。\n
        重男轻女会有什么问题呢？\n\n

        首先，这样的社会会标榜女人不求回报的付出，因为“你生为女人就有罪”；会要求女人“
        精明能干/干活麻利”，因为女人天生低人一等，娶你为了服侍丈夫老爷的嘛！（我见过好多
        福建的女孩特别能干上进，其实是对自己是女儿身的自卑的过度补偿）如果出现了“气管炎”，
        在这部分地区是十分丢人和抬不起头的事情，会被整个社会耻笑。男人如果能有好几个女人，
        是十分光荣的事情，女人要是出轨，就是十恶不赦天打雷劈——因为在这里女人最多男人价值的
        0.5嘛，那必须1个男人占有2个以上女人，才符合价值定律啊！\n

        于是，这就创造了一种可怕的代际轮回。"""
    # get cover image(also top image)
    cover_url = "https://secure.gravatar.com/avatar/0024710771815ef9b74881ab21ba4173?s=420"
    image_searcher = BaiduImage(opinion_str)
    images_url = image_searcher.get_images_url()
    if len(images_url) > 0:
        cover_url = images_url[0]
        
    img_insert_tpl = "<img src=%s /img>" % cover_url    
    html_str ="""
        <html>
            <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            <title>%s</title>
            </head>

            <body>
            <h2>%s</h2>
            <hr />
            <p>%s tabsun irumor</p>
            <br>
            %s
            <p>%s</p>
            <br>
            <p>更多内容关注irumor</p>
            <img src="http://i.imgur.com/o8L9ItZ.jpg"/>
            </body>
        </html>""" % (title_str, title_str, date_str, img_insert_tpl, content_str)

    temp_file_dir = "/var/ArticlePoolVolume/temp.html"
    html_file= open(temp_file_dir,"w")
    html_file.write(html_str)
    html_file.close()

    md5 = GetFileMd5(temp_file_dir)
    article_url = "http://tabsun-nginx-web.daoapp.io"
    if md5 is not None:        
        article_url = "http://tabsun-nginx-web.daoapp.io/%s.html" % md5
        final_file_dir = "/var/ArticlePoolVolume/%s.html" % md5
        os.rename(temp_file_dir,final_file_dir)
    
    return [
        [
            title_str,
            "I wrote WeRobot",
            cover_url,
            article_url
        ]
    ]

robot.run(host='0.0.0.0',port=80)
