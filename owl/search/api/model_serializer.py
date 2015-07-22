# coding=utf-8
#Created by dengqiuhua on 15-7-19.
from rest_framework import serializers

'''url序列化'''
class UrlResultSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    url = serializers.CharField()
    description = serializers.CharField()
    code = serializers.CharField()
    score = serializers.FloatField()

'''url序列化'''
class UrlSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    url=serializers.CharField()

'''url序列化'''
class LocationSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    url=UrlSerializer()
    #click_counts= serializers.IntegerField()
    #createtime=serializers.IntegerField()