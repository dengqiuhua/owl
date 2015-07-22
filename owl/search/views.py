# coding=utf-8
from django.shortcuts import render
from django.template import RequestContext
from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect,Http404
from owl.spider.models import UrlInfo

# Create your views here.

'''查询首页'''

class Index(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}
        return render_to_response("search-index.html",context, context_instance = RequestContext(request))


'''查询结果页'''

class Searching(TemplateView):
    def get(self, request, *args, **kwargs):
        if "kw" in request.GET and request.GET["kw"]:
            keywords = request.GET["kw"].strip()
            context = {"keywords" : keywords}
        else:
            return HttpResponseRedirect(reverse("site-index"))
        return render_to_response("search-result.html",context, context_instance = RequestContext(request))

'''跳转链接'''

class Link(TemplateView):
    def get(self, request, *args, **kwargs):
        if "url" in request.GET and request.GET["url"]:
            url = request.GET["url"].strip()
            try:
                urlinfo = UrlInfo.objects.get(url_encrypt=url)
            except:
                raise Http404
            urlinfo.addClick()
            return HttpResponseRedirect(urlinfo.url)
        return HttpResponseRedirect(reverse("site-index"))
