# -*- coding:utf-8 -*-
import werobot
import time
from string import Template
from BaiduImageSearch import BaiduImage
from BaiduSearch import BaiduSearch
from goose import Goose
from goose.text import StopWordsChinese
import hashlib
import os

def log_this(name, content):
    f = open("%s.txt" % name, "w")
    f.write(content)
    f.close()
    return

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

def GetTitleContent(opinion):
    searcher = BaiduSearch(opinion) 
    results_pair = searcher.originalURLs
    # default title & description & content
    title = results_pair[0][1]
    content = """在想当初，后汉三国年间，有一位莽撞人。
                自桃园三结义以来，大爷，姓刘名备字玄德，家住大树楼桑；二弟，姓关名羽字云长，家住山西蒲州解梁县；
                三弟，姓张名飞字翼德，家住涿州范阳郡；后续四弟，姓赵名云字子龙，家住真定府常山县，百战百胜，
                后称为常胜将军。\n 
                只皆因，长坂坡前，一场鏖战，那赵云，单枪匹马，闯入曹营，砍倒大纛两杆，夺槊三条，马落陷坑，堪堪废命。
                曹孟德在山头之上见一穿白小将，白盔白甲白旗号，坐骑白龙马，手使亮银枪，实乃一员勇将。
                心想：我若收服此将，何愁大事不成！心中就有爱将之意，暗中有徐庶保护赵云，那徐庶自进得曹营，一语未发。
                今见赵将军马落陷坑、堪堪废命，口尊：“丞相莫非有爱将之意？”曹操言道：“正是”。
                徐庶言道：“何不收留此将！”曹操闻听，急忙传令：“令出山摇动，三军听分明，我要活赵云，不要死子龙。
                倘有一兵一将伤损赵将军之性命！八十三万人马，五十一员战将，与他一人抵命。”众将闻听，不敢近前，唯有后退。
                赵云，一仗怀揣幼主；二仗常胜将军之特勇，杀了个七进七出，这才闯出重围。\n 
                曹操一见，这样勇将，焉能放走？在后面紧紧追赶！追至在当阳桥前，张飞赶到，高叫：“四弟不必惊慌，
                某家在此，料也无妨！”让过赵云的人马。曹操赶到，不见赵云，只见一黑脸大汉，立于桥头之上。
                曹操忙问夏侯惇：“这黑脸大汉，他是何人”？夏侯惇言道：“他乃张飞，一‘莽撞人’。”曹操闻听，大吃一惊：
                想当初关羽在白马坡斩颜良诛文丑之时，曾对某家言道：他有一结拜三弟，姓张名飞，字翼德，
                在百万军中，能取上将之首级，如探囊取物，反掌观纹一般。今日一见，果然英勇。来呀，撤去某家青罗伞盖，
                观一观那莽撞人的武艺如何？” \n
                青罗伞盖撤下，只见张飞：
                豹头环眼、面如润铁、黑中透亮、亮中透黑、海下扎里扎煞一部黑钢髯，犹如钢针、恰似铁线。
                头戴镔铁盔、二龙斗宝，朱缨飘洒，上嵌八宝——云、罗、伞、盖、花、罐、鱼、长。
                身披锁子大叶连环甲，内衬皂罗袍，足登虎头战靴，跨下马万里烟云兽，手使丈八蛇矛，站在桥头之上，
                咬牙切齿，捶胸愤恨，大骂：“曹操听真，呔！现有你家张三爷在此，尔或攻或战、或进或退、或争或斗；
                不攻不战、不进不退、不争不斗，尔乃匹夫之辈！”
                大喊一声，曹兵吓退；大喊二声，顺水横流；大喊三声，把当阳桥喝断。
                后人有诗赞之曰：“长坂坡（当阳桥）前救赵云，吓退曹操百万军，姓张名飞字翼德，
                万古留芳莽撞人”！"""
    description = "在想当初，后汉三国年间，有一位莽撞人。"

    
##    goo = Goose({'stopwords_class': StopWordsChinese})
##    init_len = 0
##    i = 0
##    while i < min(5, len(results_pair)):
##        result_pair = results_pair[i]
##        cur_url = result_pair[0]
##        cur_article = goo.extract(url=cur_url)
##        if len(cur_article.cleaned_text) > init_len:
##            title = cur_article.title
##            description = cur_article.meta_description
##            content = cur_article.cleaned_text.encode('utf-8')
##            init_len = len(cur_article.cleaned_text)
    
    return title, content, description

def GetImagesURL(opinion):
    cover_url = "https://secure.gravatar.com/avatar/0024710771815ef9b74881ab21ba4173?s=420"
    image_searcher = BaiduImage(opinion)
    images_url = image_searcher.get_images_url()
    if len(images_url) > 0:
        cover_url = images_url[0]
        return cover_url, images_url
    else:
        return None
    
def Generate(title, date, content, images):
    # TODO: insert other images into the article
    cti = ""
    split_flag = "。"
    image_cnt = 0
    while content.find(split_flag) != -1 or image_cnt >= len(images):
        pre = content[:content.find(split_flag)+len(split_flag)]
        content = content[content.find(split_flag)+len(split_flag):]
        pre = "<br><img src=%s/%s /img><br><p>%s</p>" % ("http://tabsun-nginx-web.daoapp.io", images[image_cnt], pre)
        cti = cti + pre
        image_cnt += 1
        if image_cnt >= len(images):
            pre = "<p>%s</p>" % content
            cti = cti + pre
            break
            
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
            <br>
            <p>更多内容关注irumor</p>
            <img src="http://i.imgur.com/o8L9ItZ.jpg"/>
            </body>
        </html>""" % (title, title, date, cti)
    return html_str

# weixin server
robot = werobot.WeRoBot(token='tabsunirumor', enable_session=True)


@robot.subscribe
def subscribe(message):
    return '欢迎关注irumor！'

@robot.text
def articles(message):
    # max saved html number
    max_number = 10
    opinion_str = message.content  
    opinion_str = opinion_str.encode('utf-8')
    # get date
    date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    # get article's title and content about the opinion
    title, content, description = GetTitleContent(opinion_str)
    # get cover image(also top image)
    cover, images = GetImagesURL(opinion_str)
    cover = "http://tabsun-nginx-web.daoapp.io/" + cover
    
    # generate html content string
    html_str = Generate(title, date, content, images)
    # write the html string into html file
    temp_file_dir = "/var/ArticlePoolVolume/temp.html"
    html_file= open(temp_file_dir,"w")
    html_file.write(html_str)
    html_file.close()
    # rename html file by its MD5 and record its images and birth-second
    md5 = GetFileMd5(temp_file_dir)
    article_url = "http://tabsun-nginx-web.daoapp.io"
    if md5 is not None:
        # rename
        article_url = "http://tabsun-nginx-web.daoapp.io/%s.html" % md5
        final_file_dir = "/var/ArticlePoolVolume/%s.html" % md5
        if os.path.exists(final_file_dir):
            os.remove(temp_file_dir)
        else:
            os.rename(temp_file_dir,final_file_dir)
            # log its images
            log_dir = "/var/ArticlePoolVolume/%s.txt" % md5
            log_file = open(log_dir,"w")
            for image in images:
                log_file.write("%s\n" % image)
            log_file.close()
            # log its birth-second
            f = open("/var/ArticlePoolVolume/birth-second.txt","a")
            birth = "%s\n" % md5
            f.write(birth)
            f.close()
            # remove over-flow lines
            with open("/var/ArticlePoolVolume/birth-second.txt") as fin:
                lines = fin.readlines()
                if len(lines) > max_number:
                    md5 = lines[0][:-1]
                    # remove html
                    os.remove("/var/ArticlePoolVolume/%s.html" % md5)
                    # remove images and log
                    with open("/var/ArticlePoolVolume/%s.txt" % md5) as image_log:
                        for each_image in image_log.readlines():
                            os.remove("/var/ArticlePoolVolume/%s" % each_image[:-1])
                    os.remove("/var/ArticlePoolVolume/%s.txt" % md5)
                    # remove its info in birth-second
                    fout = open("/var/ArticlePoolVolume/new-birth-second.txt","w")
                    for lid in range(1,len(lines)):
                        fout.write(lines[lid])
                    fout.close()
            if os.path.exists("/var/ArticlePoolVolume/new-birth-second.txt"):
                os.remove("/var/ArticlePoolVolume/birth-second.txt")
                os.rename("/var/ArticlePoolVolume/new-birth-second.txt","/var/ArticlePoolVolume/birth-second.txt")  
    return [
        [
            title,
            description,
            cover,
            article_url
        ]
    ]

robot.run(host='0.0.0.0',port=80)
