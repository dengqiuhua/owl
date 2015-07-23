# coding=utf-8
#Created by dengqiuhua on 15-7-15.
import urllib2
import re
from bs4 import BeautifulSoup

def crawl(url):
   page = urllib2.urlopen(url)
   contents = page.read()
   soup = BeautifulSoup(contents,"html.parser")
   print(u'豆瓣电影250: 序号 \t影片名\t 评分 \t评价人数')
   for tag in soup.find_all('div', class_='item'):
       m_order = int(tag.find('em').get_text())
       m_name = tag.a.get_text()
       m_year = tag.span.get_text()
       m_rating_score = float(tag.em.get_text())
       m_rating_num = 5 #int(tag.find('span').get_text())
       print("%s %s %s %s %s" % (m_order, m_name, m_year, m_rating_score, m_rating_num))

def cut(sentence):
    if not ( type(sentence) is unicode):
        try:
            sentence = sentence.decode('utf-8')
        except:
            sentence = sentence.decode('gbk')
    blocks = re.split(ur"([^\u4E00-\u9FA5]+)",sentence)
    result = []
    for blk in blocks:
        tmp = re.split(ur"[^a-zA-Z0-9+#]",blk)
        result.extend([x for x in tmp if x.strip()!=""])
        #result.append(blk)

        '''if re.match(ur"[\u4E00-\u9FA5]+",blk):
            result.extend(__cut(blk))
        else:
            tmp = re.split(ur"[^a-zA-Z0-9+#]",blk)
            result.extend([x for x in tmp if x.strip()!=""])'''
    return result

def crawl2(url):
    page = urllib2.urlopen(url)
    contents = page.read()
    soup = BeautifulSoup(contents,"html.parser")
    text = get_tag(soup.body,[])

    print text

'''解析HTML内容'''

def get_content(soup, depth=0):
    #if depth > 17:return ""
    v = soup.string
    if v == None:
        c = soup.contents
        text = ""
        for t in c:
            subtext = get_content(t, depth+1)
            text += subtext + '\n'
        return text
    else:
        return v.strip()

def get_tag(soup, tags):
    #if depth > 17:return ""
    v = soup.string
    if v == None:
        c = soup.contents
        text = ""
        for t in c:
            if t.name == "a":
                tags.append(t.name)
            get_tag(t, tags)
            #text += subtext + '\n'
        return tags
    else:
        return tags

def separatewords(text):
    if not text:return []
    text_list = []
    if not type(text) is unicode:
        try:
            text = unicode(text,"utf-8")
        except:
            text = text.decode("gbk")
    #return text
    # 提取中文
    blocks = re.split(ur"([^\u4E00-\u9FA5]+)",text)
    for block_words in blocks:
        if re.match(ur"[\u4E00-\u9FA5]+",block_words):
            lenth = len(block_words)
            for i in range(lenth):
                text_list.append(block_words[i])
    return text_list

if __name__ == '__main__':
    pass
    #crawl('http://movie.douban.com/top250?format=text')
    #crawl2("http://jyzh.sinaapp.com/news/1/")
    #print cut('我们都是好孩子。')