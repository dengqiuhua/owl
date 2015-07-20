# coding=utf-8
#Created by dengqiuhua on 15-7-15.
from django.conf.urls import url,patterns
from owl.search.views import *

urlpatterns = patterns(
    '',
    #url(r'^$', Index.as_view(), name="search-index"),
    url(r'^$', Searching.as_view(), name="search-result"),

)
