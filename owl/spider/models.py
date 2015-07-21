# coding=utf-8
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UrlInfo(models.Model):
    class Meta:
        db_table = 'spider_url_info'
    url = models.CharField(max_length=300,unique=True)
    url_encrypt = models.CharField(max_length=30,unique=True)
    click_counts = models.IntegerField(default=0,null=True)
    createtime = models.IntegerField(null=True)

    @staticmethod
    def isIndexed(url_encrypt):
        return UrlInfo.objects.filter(url_encrypt=url_encrypt).count() > 0


class WordInfo(models.Model):
    class Meta:
        db_table = 'spider_word_info'
    word = models.CharField(max_length=30,db_index=True)
    spell = models.CharField(max_length=30,null=True)
    code = models.IntegerField(null=True)
    lang = models.CharField(max_length=10,null=True)
    score = models.IntegerField(default=0 , null=True)

class WordLocation(models.Model):
    class Meta:
        db_table = 'spider_word_location'
    url = models.ForeignKey(UrlInfo)
    word = models.ForeignKey(WordInfo)
    location = models.IntegerField(default=-1,null=True)
    location_type = models.IntegerField(default=0,null=True)#title,keywords,description,content

class LinkInfo(models.Model):
    class Meta:
        db_table = 'spider_link_info'
    from_url = models.ForeignKey(UrlInfo)
    to_url = models.ForeignKey(UrlInfo,related_name="to")
    createtime = models.IntegerField(null=True)

    @staticmethod
    def isExist(url_from,url_to):
        return LinkInfo.objects.filter(from_url=url_from,to_url=url_to).count() > 0

class LinkWords(models.Model):
    class Meta:
        db_table = 'spider_link_words'

    link = models.ForeignKey(LinkInfo)
    word = models.ForeignKey(WordInfo,null=True)