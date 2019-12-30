from django.shortcuts import render
import tree
import pickle as pk

def write2pk(obj,path):
    with open(path,'wb') as f:
        pk.dump(obj,f)

def readpk(path):
    with open(path,'rb') as f:
        obj=pk.load(f)
    return obj


class InnerObj:
    def __init__(self,obj):
        print(obj)
        self.title=obj['主标题']
        self.image=obj['图片']
        self.writer=obj.get(' 作者','')
        self.publishier=obj.get('出版社','')
        self.subtitle=obj.get('副标题:','')
        self.translater=obj.get(' 译者','')
        self.date=obj.get('出版年:','')
        self.pages=obj.get('页数:','')
        self.price=obj.get('定价:','')
        self.wrap=obj.get('装帧:','')
        self.other=obj.get('丛书:','')
        self.isbn=obj.get('ISBN:','')


# Create your views here.
 
def index(request):
    context={}
    context['objlist']=[]
    return render(request,'index.html',context)

def search(request):
    key=request.GET.get('key','')
    T=readpk('T.pk')
    ret=T.search(key)
    context={}
    context['objlist']=[]
    if(ret['kind']=='Lnode'):
        print(ret['ret'])
        path=ret['ret'].obj['path']
        obj=readpk(path)
        innerobj=InnerObj(obj)
        context['objlist'].append(innerobj)
    return render(request,'index.html',context)