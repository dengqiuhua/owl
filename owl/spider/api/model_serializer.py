# coding=utf-8
#Created by dengqiuhua on 15-7-19.
from rest_framework import serializers

'''url序列化'''
class UrlSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    url=serializers.CharField()
    click_counts= serializers.IntegerField()
    createtime=serializers.IntegerField()