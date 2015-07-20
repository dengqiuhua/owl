# coding=utf-8
#Created by dengqiuhua on 15-7-18.
from rest_framework.views import APIView
from owl.spider.api.crawl import Crawl
from owl.spider.models import UrlInfo
from owl.scripts.func import GetResponseData,getPageSizeAndIndex
from model_serializer import UrlSerializer

class CrawlPages(APIView):
    def get(self, request, **kwargs):
        if 'url' in request.GET and request.GET['url']:
            url = request.GET['url'].strip()
        #分页
        pagesize, pageindex = getPageSizeAndIndex(request)
        args = {}
        datalist = UrlInfo.objects.filter(**args).order_by("-createtime")[(pageindex - 1) * pagesize:pagesize * pageindex]
        counts = UrlInfo.objects.filter(**args).count()
        data=UrlSerializer(datalist).data
        return GetResponseData(True,0,data,counts)

    def post(self, request, **kwargs):
        if 'url' in request.POST and request.POST['url']:
            url = request.POST['url'].strip()
            res = Crawl().main([url])
            return GetResponseData(True,0,res)
        return GetResponseData(False)

