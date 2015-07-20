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

if __name__ == '__main__':
    #crawl('http://movie.douban.com/top250?format=text')
    print cut('我们都是好孩子。')