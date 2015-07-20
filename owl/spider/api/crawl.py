# coding=utf-8
#Created by dengqiuhua on 15-7-18.
from owl.scripts.func import singleton,md5
from bs4 import BeautifulSoup
from urlparse import urljoin
from owl.spider.models import UrlInfo,WordInfo,WordLocation,LinkInfo,LinkWords
import urllib2,time,sys

@singleton
class Crawl(object):
    ignorewords = ["的","了","是","就","吗","呢","啊","，","。","？","；","《","》","：",".","（","）","“","”","／","<",">","……","＃","$","％","@","-"]

    def __init__(self):
        #递归数
        sys.setrecursionlimit(10000)

    def main(self,urllist,dep=0):
        for domain in urllist:
            #爬行
            try:
                c = urllib2.urlopen(domain)
            except:
                continue
            #是否发生重定向
            redirected = c.geturl() != domain
            if redirected:
                continue
            soup = BeautifulSoup(c.read(),"html.parser")
            self.add_index(domain,soup)

            # 查找其他链接
            links = soup.find_all("a")
            filter_links = ["","javascript:;","#","javascript:void(0);"]
            if links:
                newpages = []
                for link in links:
                    if 'href' in dict(link.attrs) and link["href"] not in filter_links:
                        url = urljoin(domain,link["href"])
                        if url.find("'") != -1:continue
                        url = url.split("#")[0]
                        if url[0:4] == "http" and url != domain :
                            if not UrlInfo.isIndexed(md5(url)):
                                newpages.append(url)
                            link_text = self.get_content(link)
                            # 添加到链接来源
                            self.add_link(domain,url,link_text)
                #递归获取
                if newpages and dep <2:
                    pass
                    #self.main(newpages, dep+1)
                else:
                    return
            else:
                continue
        return True



    def add_index(self,domain,soup):
        url_encrypt = md5(domain)
        if UrlInfo.isIndexed(url_encrypt):return
        # 插入url
        urlinfo = UrlInfo.objects.create(url=domain,url_encrypt=url_encrypt,createtime=time.time())
        #start_index = 0
        # 提取title
        text_title = soup.html.head.title
        text_title_list = self.separatewords(text_title)
        self.add_location(urlinfo,text_title_list,1)
        # 获取关键字
        text_keywords = soup.html.head.keyword
        text_keywords_list = self.separatewords(text_keywords)
        self.add_location(urlinfo,text_keywords_list,2)
        # 获取描述
        text_description = soup.html.head.description
        text_description_list = self.separatewords(text_description)
        self.add_location(urlinfo,text_description_list,3)
        # 获取内容
        text_content = self.get_content(soup.body)
        text_content_list = self.separatewords(text_content)
        self.add_location(urlinfo,text_content_list,4)

    '''提取分词'''

    def separatewords(self,text):
        sys.setrecursionlimit(10000)
        lenth = len(text)
        text_list = []
        if not type(text) is unicode:
            try:
                text = unicode(text,"utf-8")
            except:
                text = unicode(text,"gbk")
        # 提取中文
        blocks = re.split(ur"([^\u4E00-\u9FA5]+)",sentence)
        for block_words in blocks:
            if re.match(ur"[\u4E00-\u9FA5]+",block_words):
                for i in range(lenth):
                    text_list.append(block_words[i])
                return text_list

    def add_location(self,urlinfo,words,type = 0):
        if not words:return
        counts = len(words)
        for i in range(counts):
            if words[i] in self.ignorewords:continue
            word = self.get_word(words[i])
            if word:
                WordLocation.objects.create(url=urlinfo,word=word,location=i,location_type=type)

    def add_link(self,from_url,to_url,link_text):
        try:
            url_from = UrlInfo.objects.get(url_encrypt=md5(from_url))
            url_to = UrlInfo.objects.get(url_encrypt=md5(to_url))
        except:
            return
        if url_from == url_to or LinkInfo.isExist(url_from,url_to) : return
        linkinfo = LinkInfo.objects.create(from_url=url_from,to_url=url_to,createtime=time.time())
        if link_text:
            words = self.separatewords(link_text)
            for word in words:
                LinkWords.objects.create(link=linkinfo,word=word)


    def get_word(self,word):
        words = WordInfo.objects.filter(word=word)
        if words:
            return words[0]
        return None


    def get_content(self, soup, depth=0):
        if depth > 17:return ""
        v = soup.string
        if v == None:
            c = soup.contents
            text = ""
            for t in c:
                subtext = self.get_content(t, depth+1)
                text += subtext + '\n'
            return text
        else:
            return v.strip()

#if __name__ == '__main__':
    #Crawl().main(['http://movie.douban.com/top250?format=text'])




