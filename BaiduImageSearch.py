# -*- coding:utf-8 -*-
#coding=utf-8
from urllib import quote
import urllib2 as urllib
import random
import re
import os
import hashlib

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

class BaiduImage():

    def __init__(self, keyword, count=10, save_path="img", rn=60):
        self.keyword = keyword
        self.count = count
        self.save_path = save_path
        self.rn = rn

        self.__imageList = []

        self.__encodeKeyword = quote(keyword)
        self.__acJsonCount = self.__get_ac_json_count()

        self.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"
        self.headers = {'User-Agent': self.user_agent, "Upgrade-Insecure-Requests": 1,
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                        "Accept-Encoding": "gzip, deflate, sdch",
                        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
                        "Cache-Control": "no-cache"}
        
    def search(self):
        for i in range(0, self.__acJsonCount):
            url = self.__get_search_url(i * self.rn)
            response = self.__get_response(url)            
            image_url_list = self.__pick_image_urls(response)
            self.__imageList.extend(image_url_list)

    def get_images_url(self, keyword):
        self.search()
        num = random.randint(4, 6)
        urls = []
        count = 0
        for each_url in self.__imageList:
            host = self.get_url_host(each_url)
            self.headers["Host"] = host
            if count < num:
                try:
                    # get image into /var/vo directory and rename it by its md5
                    req = urllib.Request(each_url, headers=self.headers)
                    data = urllib.urlopen(req, timeout=20)

                    image_name = "/var/ArticlePoolVolume/images/%d.jpg" % count
                    tmp_file = open(image_name,"wb")
                    tmp_file.write(data.read())
                    tmp_file.close()
                    if not os.path.isfile(image_name):
                        continue
                    else:
                        image_md5 = GetFileMd5(image_name)
                        new_name = "/var/ArticlePoolVolume/images/%s.jpg" % image_md5
                        if not os.path.exists(new_name):
                            os.rename(image_name, new_name)
                        else:
                            os.remove(image_name)
                        real_url = "images/%s.jpg" % image_md5
                        urls.append(real_url)
                        count += 1
                except Exception as e:
                    count += 0
            else:
                break
        return urls

    def __pick_image_urls(self, response):
        #reg = r'"ObjURL":"(http.*?)"'
        reg = r'"thumbURL":"(.*?)"'
        imgre = re.compile(reg)
        imglist = re.findall(imgre, response)
        #real_urls = []
        #for link in imglist:
        #    if "imgtn.bdimg.com" not in link:
        #        real_urls.append(link.replace("\/","/"))
        return imglist

    def __get_response(self, url):
        page = urllib.urlopen(url)
        return page.read()

    def __get_search_url(self, pn):
        return "http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=" + self.__encodeKeyword + "&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word=" + self.__encodeKeyword + "&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&pn=" + str(pn) + "&rn=" + str(self.rn) + "&gsm=1000000001e&1486375820481="

    def get_url_host(self, url):
        reg = r'http://(.*?)/'
        hostre = re.compile(reg)
        host = re.findall(hostre, url)
        if len(host) > 0:
            return host[0]
        return ""

    def __get_ac_json_count(self):
        a = self.count % self.rn
        c = self.count / self.rn
        if a:
            c += 1
        return c
