# -*- coding:utf-8 -*-
from pyquery import PyQuery as pq
from urlparse import urlparse
import requests

class BaiduNewsSearch:
    def __init__(self, keyword, method='GET', **kwargs):
        url = 'http://news.baidu.com/ns?cl=2&rn=20&tn=news&word=%s' % keyword
        headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
        self.host = urlparse(url).scheme+'://'+urlparse(url).netloc
        self.rep = requests.request(url=url, method=method,headers = headers, verify=False, **kwargs)
        self.method = method
        self.headers = self.rep.request.headers
        self.ok = self.rep.ok
        self.url = self.rep.url
        self.text = self.rep.text
        self.doc = pq(self.rep.content)
        try:
            self.json = self.rep.json()
        except:
            self.json = {}
        self.cookies = self.rep.cookies

    def get_results(self):
        results = []
        for each_pair in self.doc('.c-title a').items():
            results.append((each_pair.attr.href,each_pair.text()))
        return results
