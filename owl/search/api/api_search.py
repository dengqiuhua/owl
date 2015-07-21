# coding=utf-8
#Created by dengqiuhua on 15-7-21.
from rest_framework.views import APIView
from owl.search.api.search import Search
from owl.scripts.func import GetResponseData,getPageSizeAndIndex
from model_serializer import UrlSerializer,LocationSerializer

'''搜索'''

class SearchResult(APIView):
    def get(self, request, **kwargs):
        if 'kw' in request.GET and request.GET['kw']:
            keywords = request.GET['kw'].strip()
            #分页
            pagesize, pageindex = getPageSizeAndIndex(request)
            args = {}
            datalist,counts = Search().getResult(keywords,pagesize, pageindex)
            data=LocationSerializer(datalist).data
            return GetResponseData(True,0,data,counts)
        return GetResponseData(False,-3)