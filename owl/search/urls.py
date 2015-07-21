# coding=utf-8
#Created by dengqiuhua on 15-7-15.
from django.conf.urls import url,patterns
from owl.search.views import *
from owl.search.api.api_search import SearchResult

urlpatterns = patterns(
    '',
    #url(r'^$', Index.as_view(), name="search-index"),
    url(r'^s/$', Searching.as_view(), name="search-result"),
    url(r'^api/search/$', SearchResult.as_view(), name="api-search-result"),

)
