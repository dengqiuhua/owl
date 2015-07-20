# coding=utf-8
#Created by dengqiuhua on 15-7-15.
from django.conf.urls import url,patterns
from owl.spider.views import *
from owl.spider.api.api_crawl import CrawlPages

urlpatterns = patterns(
    '',
    url(r'^$', Index.as_view(), name="spider-index"),
    url(r'^crawl/$', Crawl.as_view(), name="spider-crawl"),
    url(r'^list/$', Spidering.as_view(), name="spider-list"),
    #爬行接口
    url(r'^api/crawl/$', CrawlPages.as_view(), name="api-spider-crawl"),

)
