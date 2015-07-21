# coding=utf-8
from owl.scripts.func import singleton,md5
from owl.spider.models import UrlInfo,WordInfo,WordLocation,LinkInfo,LinkWords
from django.db.models import Q, Max, Min, Count
import re

@singleton
class Search(object):

    def getResult(self,kw,pageindex = 1, pagesize = 10):
        keywords = self.separatewords(kw)
        if keywords:
            #wordlist = WordInfo.objects.filter(word__in=keywords)
            #keywords = [u"美",u"课"]
            wordlist = []
            for word in keywords:
                try:
                    wordinfo = WordInfo.objects.get(word=word)
                except:
                    continue
                wordlist.append(wordinfo)
            location = WordLocation.objects.filter(word__in = wordlist).order_by("location")[(pageindex - 1) * pagesize:pagesize * pageindex]#.query.group_by("url")#
            return location,location.count()
        return [],0

    '''提取分词'''

    def separatewords(self,text):
        if not text:return []
        text_list = []
        if not type(text) is unicode:
            try:
                text = unicode(text,"utf-8")
            except:
                text = text.decode("gbk")
        # 提取中文
        blocks = re.split(ur"([^\u4E00-\u9FA5]+)",text)
        for block_words in blocks:
            if re.match(ur"[\u4E00-\u9FA5]+",block_words):
                lenth = len(block_words)
                for i in range(lenth):
                    text_list.append(block_words[i])
                return text_list