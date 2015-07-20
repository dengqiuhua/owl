# coding=utf-8
#Created by dengqiuhua on 15-7-18.
from rest_framework.response import Response
import hashlib,datetime,random,uuid

'''单例方法'''

def singleton(cls, *args, **kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton

'''获取MD5加密'''

def md5(code):
    return hashlib.md5(code.encode("utf-8")).hexdigest()

'''获取分页的页码'''

def getPageSizeAndIndex(request):
    pagesize = 10
    pageindex = 1
    if 'pagesize' in request.GET:
        pagesize = int(request.GET['pagesize'])
    if 'pageindex' in request.GET:
        pageindex = int(request.GET['pageindex'])
    return pagesize,pageindex

'''随机验证码'''
def getRandCode(length=0,isdigit=False):
    feed=["1","2","3","4","5","6","7","8","9","0","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    code=""
    if isdigit:
        feed=range(0, 11)
        if length == 0:
            code="%d%d%d%d" % (datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day,random.randint(10000, 99999))
        else:
            for i in range(1, length + 1):
                item = random.choice(feed)
                code += str(item)
        return code
    else:
        if length==0:
            code = str(uuid.uuid1()).replace('-','')
        else:
            for i in range(1, length + 1):
                item = random.choice(feed)
                code += item
        return code

'''格式化返回数据格式json'''
def GetResponseData(result,error_code=0,data=None,counts=None):
    context={}
    context['result']=result
    context['data']=data
    context['code']=error_code
    if error_code and error_code !=0:
        context['error']='error'#ErrorMsg[error_code]
    if counts or counts==0:
        context['counts']=counts
    return Response(context)