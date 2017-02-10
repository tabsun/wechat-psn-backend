# -*- coding:utf-8 -*-
import sys
import re
import requests
from pyquery import PyQuery as Pq

class BaiduSearch(object):
    
    def __init__(self, searchText):
        self.url = "http://www.baidu.com/baidu?wd=%s&tn=monline_4_dg" % searchText
        self.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17"}
        self._page = None
    
    @property 
    def page(self):
        if not self._page:
            r = requests.get(self.url, headers=self.headers)
            r.encoding = 'utf-8'
            self._page = Pq(r.text)
        return self._page
    
    @property
    def baiduURLs(self):
        return [(site.attr('href'), site.text().encode('utf-8')) for site in self.page('div.result.c-container  h3.t  a').items()]
    
    @property    
    def originalURLs(self):
        tmpURLs = self.baiduURLs
        originalURLs = []
        for tmpurl in tmpURLs:
            tmpPage = requests.get(tmpurl[0], allow_redirects=False)
            if tmpPage.status_code == 200:
                urlMatch = re.search(r'URL=\'(.*?)\'', tmpPage.text.encode('utf-8'), re.S)
                originalURLs.append((urlMatch.group(1), tmpurl[1]))
            elif tmpPage.status_code == 302:
                originalURLs.append((tmpPage.headers.get('location'), tmpurl[1]))
            else:
                print 'No URL found!!'
        results = []
        for each_pair in originalURLs:
            url = each_pair[0]
            title = each_pair[1]
            title = title.split("_")[0]
            results.append((url,title))
        return results

searchText = "35岁之后不适合生孩子"

bdsearch = BaiduSearchSpider(searchText) 
originalurls = bdsearch.originalURLs

output = open('result.txt','w')
for result in originalurls:
    output.write("---------------------------\n")
    output.write(result[0])
    output.write("\n")
    output.write(result[1])
    output.write("\n")
    output.write("---------------------------\n")
output.close()
print '============================'
