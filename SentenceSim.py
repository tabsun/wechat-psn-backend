# -*- coding: utf-8 -*- 
import math

class SentenceSim():
    def __init__(self, filename):
        self.d = {}
        self.log = lambda x: float('-inf') if not x else math.log(x)
        self.prob = lambda x: self.d[x] if x in self.d else 0 if len(x)>1 else 1
        self.d['_t_'] = 0.0
        with open(filename, 'r') as handle:
            for line in handle:
                word, freq = line.split('\t')[0:2]
                self.d['_t_'] += int(freq)+1
                try:
                    self.d[word.decode('gbk')] = int(freq)+1
                except:
                    self.d[word] = int(freq)+1
 
    def solve(self, s):
        l = len(s)
        p = [0 for i in range(l+1)]
        t = [0 for i in range(l)]
        for i in xrange(l-1, -1, -1):
            p[i], t[i] = max((self.log(self.prob(s[i:i+k])/self.d['_t_'])+p[i+k], k) \
                        for k in xrange(1, l-i+1))
        while p[l]<l:
            yield s[p[l]:p[l]+t[p[l]]]
            p[l] += t[p[l]]

    def cos_dist(self, a, b):
        if len(a) != len(b):
            return None
        part_up = 0.0
        a_sq = 0.0
        b_sq = 0.0
        for a1, b1 in zip(a,b):
            part_up += a1*b1
            a_sq += a1**2
            b_sq += b1**2
        part_down = math.sqrt(a_sq*b_sq)
        if part_down == 0.0:
            return None
        else:
            return part_up / part_down

    def get_sim(self, s1, s2):
        s1 = unicode(s1, 'utf-8')
        s2 = unicode(s2, 'utf-8')
        s1 = list(self.solve(s1))
        s2 = list(self.solve(s2))
        key=list(set(s1+s2))
        
        keyLen=len(key)
        keyValue=0
 
        sk1=[keyValue]*keyLen
        sk2=[keyValue]*keyLen
    
        for index,keyElement in enumerate(key):
            if keyElement in s1:
                sk1[index]=sk1[index]+1
            if keyElement in s2:
                sk2[index]=sk2[index]+1
        return self.cos_dist(sk1,sk2)
    
if __name__ == '__main__':
    ssim = SentenceSim('SogouLabDic.dic')
    sentence1 = "周杰伦是一个歌手,也是一个叉叉"
    sentence2= "周杰伦不是一个叉叉，但是是一个歌手"

    print ssim.get_sim(sentence1, sentence2)
    
