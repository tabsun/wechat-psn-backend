# -*- coding:utf-8 -*-
import urllib  
import urllib2
import zlib
import cookielib
import re
import sys
import numpy as np
import pylab as pl

class Html2Article():
    def __init__(self):
        self.threshold = 480
        self.charset_type_list = ['gbk','gb2312','utf-8','utf-16','ascii']

    def detect_possible_type(self, html):
        re_type = re.compile(r'charset=".*?"')
        char_type = re_type.search(html).group()
        if len(char_type) >= 10:
            char_type = char_type[9:-1].upper()
        else:
            char_type = None
        return char_type
    
    def get_html(self, url):
        cookie = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}  
        request = urllib2.Request(url=url,headers=headers)
        request.add_header('Accept-encoding', 'gzip,utf-8')
        
        response = opener.open(request)
        html = response.read()
        gzipped = response.headers.get('Content-Encoding')
        if gzipped:
            html = zlib.decompress(html, 16+zlib.MAX_WBITS)

        return html

    def html2article(self,html_file):
        # remove the flags
        tempResult = re.sub('<script([\s\S]*?)</script>','',html_file)
        tempResult = re.sub('<style([\s\S]*?)</style>','',tempResult)
        tempResult = re.sub('(?is)<.*?>','',tempResult)
        tempResult = tempResult.replace(' ','')
        tempResultArray = tempResult.split('\n')
        
        data = []
        string_data = []
        result_data = ""
        summ = 0
        count = 0

        #calculate non-zero line and their length
        for oneLine in tempResultArray:
            if(len(oneLine)>0):
                data.append(len(oneLine))
                string_data.append(oneLine)
                summ += len(oneLine)
                count += 1
            
        for oneLine in string_data:
            if len(oneLine) >= self.threshold:
                result_data += oneLine

        if len(result_data) == 0:
            return None
        else:
            return result_data

    def get_article(self,url):
        # get original html data
        html_data = self.get_html(url)
        if not html_data:
            return None
           
        # loop all charset type to get the content
        cid = 0
        while cid < len(self.charset_type_list):
            cur_type = self.charset_type_list[cid]
            print "loop in ",cur_type
            have_error = False
            try:
                cur_html = html_data.decode(cur_type).encode('utf-8')
            except:
                have_error = True
                
            if not have_error:
                cur_content = self.html2article(cur_html)
                have_error = False
                try:
                    cur_content.decode('utf-8').encode('gbk')
                except:
                    have_error = True
                if cur_content is not None and (not have_error):
                    return cur_content           
            cid += 1
        # all type fail then return no-string
        return ""
            
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: python Html2Article.py <article's address>"
        exit(-1)
    convertor = Html2Article()
    content = convertor.get_article(sys.argv[1])
    if content is not None:
        print content.decode('utf-8')
        
    
