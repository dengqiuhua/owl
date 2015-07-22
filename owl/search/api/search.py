# coding=utf-8
from owl.scripts.func import singleton,md5
from owl.spider.models import UrlInfo,WordInfo,WordLocation,LinkInfo,LinkWords
#from django.db.models import Q, Max, Min, Count
from django.db import connection
from model_serializer import UrlResultSerializer
import re

@singleton
class Searcher(object):

    def Search(self,kw,pageindex = 1, pagesize = 10):
        keywords = self.separatewords(kw)
        if keywords:
            wordlist = self.getWordInfoList(keywords)
            rows = self.getMatchWordLocation(wordlist)
            rankedResult = self.getScoredList(rows)
            location = self.formatResult(rankedResult)
            #print(location)
            #return
            counts = len(location)
            return location,counts
        return [],0

    '''格式化结果'''

    def formatResult(self,datalist):
        newlist = []
        if datalist:
            for urlid,score in datalist:
                urlinfo = UrlInfo.objects.get(id=urlid)
                res = UrlResultSerializer()
                res.id = urlid
                res.url = urlinfo.url
                res.code = urlinfo.url_encrypt
                res.description = self.getDescription(urlid)
                res.score = score
                newlist.append(res)
        return newlist

    '''获取描述'''

    def getDescription(self,urlid):
        locations = WordLocation.objects.filter(url__id=urlid)
        if locations:
            desc = ""
            for location in locations:
                desc += location.word.word
            return desc
        return

    '''获取排序的结果'''

    def getScoredList(self,rows):
        if rows:
            urls = dict([(row[0],0) for row in rows])
            #各维度权重[词频，文档位置，词间距]
            weights = [(1.0, self.getFrequencyScore(rows)),(1.5, self.getLocationScore(rows)),(2.0, self.getDistanceScore(rows))]
            for weight,scores in weights:
                for url in urls:
                    urls[url] += weight * scores[url]
            # 降序排列
            rankedResults = sorted([(url,score) for url,score in urls.items()],reverse=1)
            return rankedResults
        return []

    '''根据词频排序'''

    def getFrequencyScore(self,rows):
        if rows:
            counts = dict([(row[0],0) for row in rows])
            for row in rows:
                counts[row[0]] += 1
            return self.normalizeScores(counts)
        return rows

    '''根据字在文档的位置'''

    def getLocationScore(self,rows):
        if rows:
            #填入一个标准位置
            locations = dict([(row[0],1000000) for row in rows])
            for row in rows:
                location = sum(row[1:]) # 这几个个字所有位置的总和
                # 总和小于1000000
                if location < locations[row[0]]:locations[row[0]] = location
            return self.normalizeScores(locations,True)
        return rows

    '''根据字间距'''

    def getDistanceScore(self,rows):
        if rows:
            if len(rows[0]) <= 2:return dict([(row[0], 1.0) for row in rows])
            #填入一个标准距离
            minDistance = dict([(row[0], 1000000) for row in rows])
            for row in rows:
                dlist = sum([abs(row[i] - row[i-1]) for i in range(2,len(row))])
                # 总和小于1000000
                if dlist < minDistance[row[0]] : minDistance[row[0]] = dlist
            return self.normalizeScores(minDistance,True)
        return rows

    '''归一化函数'''

    def normalizeScores(self,scores,small = False):
        vsmall = 0.0001 # 避免被0整除
        if small:
            # 越小越好
            minscore = min(scores.values())
            return dict([(url,float(minscore) / max(vsmall,counts)) for (url,counts) in scores.items()])
        else:
            maxscore = max(scores.values())
            if maxscore == 0 : maxscore = vsmall
            return dict([(url,float(counts) / maxscore) for (url,counts) in scores.items()])

    '''获取匹配的词的位置'''

    def getMatchWordLocation(self,wordlist):
        if len(wordlist) > 1:
            field = ""
            table = ""
            where_url = ""
            where_word = ""
            for i,word in enumerate(wordlist):
                field += ",w%d.location" % i
                if table == "":
                    table += " spider_word_location w%d" % i
                else:
                    table += ",spider_word_location w%d" % i
                where_url += " AND w0.url_id = w%d.url_id" % i
                where_word += " AND w%d.word_id = %d" % (i, word.id)
            sql = "SELECT w0.url_id %s FROM %s WHERE 1 = 1 %s %s ;" % (field, table, where_url, where_word)
        else:
            sql = "SELECT url_id,location FROM spider_word_location WHERE word_id = %d ;" % wordlist[0].id
        cursor = connection.cursor()
        cursor.execute(sql)
        datalist=cursor.fetchall()
        #datalist = WordLocation.objects.raw(sql)
        return datalist

    '''获取搜索关键字对应的词库'''

    def getWordInfoList(self,keywords):
        wordlist = []
        for word in keywords:
            try:
                wordinfo = WordInfo.objects.get(word=word)
            except:
                continue
            wordlist.append(wordinfo)
        return wordlist

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