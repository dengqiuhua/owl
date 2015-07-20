# coding=utf-8
from django.shortcuts import render
from django.template import RequestContext
from django.views.generic import TemplateView
from django.shortcuts import render_to_response

# Create your views here.

class Index(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}
        return render_to_response("search-index.html",context, context_instance = RequestContext(request))

class Searching(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}
        return render_to_response("search-result.html",context, context_instance = RequestContext(request))
