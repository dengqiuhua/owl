# coding=utf-8
from django.shortcuts import render,render_to_response
from django.views.generic import TemplateView
from django.template import RequestContext
from urlparse import urljoin
import urllib2
from bs4 import BeautifulSoup

class Index(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}
        context["leftnav"] = 1
        return render_to_response("spider-index.html",context, context_instance = RequestContext(request))

class Crawl(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}
        context["leftnav"] = 2
        return render_to_response("spider-crawl.html",context, context_instance = RequestContext(request))

class Spidering(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}
        context["leftnav"] = 3
        return render_to_response("spider-list.html",context, context_instance = RequestContext(request))
