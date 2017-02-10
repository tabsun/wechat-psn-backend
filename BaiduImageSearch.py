# -*- coding:utf-8 -*-
#coding=utf-8
from urllib import quote
import urllib2 as urllib
import random
import re
import os


class BaiduImage():

    def __init__(self, keyword, count=1, save_path="img", rn=60):
        self.keyword = keyword
        self.count = count
        self.save_path = save_path
        self.rn = rn

        self.__imageList = []

        self.__encodeKeyword = quote(self.keyword)
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
            # tabsun
            log = open("log.html","w")
            log.write(response)
            log.close()
            
            image_url_list = self.__pick_image_urls(response)
            self.__imageList.extend(image_url_list)

    def get_images_url(self):
        self.search()
        num = random.randint(4, 6)
        urls = []
        count = 0
        for image in self.__imageList:
            host = self.get_url_host(image)
            self.headers["Host"] = host
            if count < num:
                try:
                    #print image
                    #req = urllib.Request(image, headers=self.headers)
                    #img = urllib.urlopen(req, timeout=20)
                    real_url = image #img.geturl()
                    urls.append(real_url)
                    count += 1
                except Exception as e:
                    count += 0
            else:
                break
        return urls

    def __pick_image_urls(self, response):
        reg = r'"ObjURL":"(http.*?)"'
        imgre = re.compile(reg)
        imglist = re.findall(imgre, response)
        real_urls = []
        for link in imglist:
            if "imgtn.bdimg.com" not in link:
                real_urls.append(link.replace("\/","/"))
        return real_urls

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
