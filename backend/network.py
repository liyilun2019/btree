from html.parser import HTMLParser
from urllib.request import Request,urlopen
import time 
import queue
from tree import Tree
import pickle as pk
import os

def to_dic(lis):
    dic={}
    for (k,v) in lis:
        dic[k]=v
    return dic

def write2pk(obj,path):
    with open(path,'wb') as f:
        pk.dump(obj,f)

def readpk(path):
    with open(path,'rb') as f:
        obj=pk.load(f)
    return obj


class MyPraser(HTMLParser):
    retobj={}
    active=False
    action='no'
    curkey=''
    more=False
    links=[]
    pic=False

    def handle_starttag(self,tag,attrs):
        attrs=to_dic(attrs)
        if(tag=='div' and 'id'in attrs.keys() and attrs['id']=='info'):
            self.active=True
        if(self.active and tag=='span' and 'class' in attrs.keys()):
            self.action='key'
        if(tag=='div' and 'class' in attrs.keys() and attrs['class']=='content clearfix'):
            self.more=True

        if(tag=='div' and attrs.get('id','')=='mainpic'):
            self.pic=True
        if(self.pic and tag=='img'):
            self.retobj['图片']=attrs.get('src','')
            self.pic=False

        if(tag=='span' and attrs.get('property','')=='v:itemreviewed'):
            self.active=True
            self.curkey='主标题'
            self.action='value'


        if(self.more and tag=='a' and 'href'in attrs.keys()):
            self.links.append(attrs['href'])

    def handle_data(self,data):
        if(self.active and self.action=='key'):
            self.curkey=data
            self.action='value'
        elif(self.active and self.action=='value' and '\n' not in data and '\xa0' not in data):
            self.retobj[self.curkey]=data
            self.action='no'
    def handle_endtag(self,tag):
        if(tag=='div'):
            self.active=False
            self.more=False


class urlReader():
    def __init__(self,initurl):
        self.initurl=initurl
        self.parser=MyPraser()
        self.maxcnt=5
        self.cnt=0

    def read_once(self,url):
        r=Request(url,headers={'User-agent':'Mozilla 5.10'})
        t=urlopen(r)
        self.parser.feed(str(t.read(),encoding='utf8'))
        time.sleep(3)
        del self.parser.links[0]
        return self.parser.retobj,self.parser.links

    def start(self,callback):
        q=queue.Queue()
        q.put(self.initurl)
        visurl=[]
        vis=[]
        while not q.empty():
            l=q.get()
            if len(vis)>=self.maxcnt:
                break
            if l in visurl:
                continue
            visurl.append(l)
            obj,lks=self.read_once(l)
            if obj['主标题'] in vis:
                continue
            vis.append(obj['主标题'])
            callback(obj)
            for u in lks:
                q.put(u)

T=Tree(4)

def caller(obj):
    obj['key']=obj['主标题']
    key=obj['key']
    path=f'dataset/{key}.pk'
    path=os.path.abspath(path)
    write2pk(obj,path)
    print(key)
    T.insert({'key':key,'path':path})

if __name__=='__main__':

    a={'主标题': '欢迎来到敌托邦', ' 作者': '[英]戈登·范·格尔德', '出版社:': ' 新星出版社', '副标题:': ' 对未来的45种预见', ' 译者': '赵阳', '出版年:': ' 2019-11', '页数:': ' 424', '定价:': ' 59.00元', '装帧:': ' 平装', '丛书:': '幻象文库', 'ISBN:': ' 9787513335638', 'key': '欢迎来到敌托邦'}
    b={'主标题': '第六大陆（上下）', ' 作者': '[日] 小川一水', '出版社:': ' 新星出版社', '副标题:': ' 对未来的45种预见', ' 译 者': '曹京柱', '出版年:': ' 2016-7', '页数:': ' 564', '定价:': ' 65.00元', '装帧:': ' 平装', '丛书:': '幻象文库', 'ISBN:': ' 9787513321471', 'key': '第六大陆（上下）'}
    c={'主标题': '隐页书城（三部曲）', ' 作者': '[德] 凯·迈尔', '出版社:': ' 广西师范大学出版社', '副标题:': ' 心灵之书·永夜之国·家族之书', ' 译者': '顾牧', '出版年:': ' 2019-11', '页数:': ' 1312', '定价:': ' 165.00元', '装帧:': ' 平装', '丛书:': '幻象文库', 'ISBN:': ' 9787559821621', 'key': '隐页书城（三部曲）', '出品方:': '理想国', '原作名:': ' DIE SEITEN DER WELT'}
    d={'主标题': '沙德维尔的暗影', ' 作者': '[英]詹姆斯·洛夫格罗夫', '出版社:': ' 浙江文艺出版社', '副标题:': ' Shadwell Shadows', ' 译者': '王予润', '出版年:': ' 2019-12', '页数:': ' 386', '定价:': ' 49.8', '装帧:': ' 平装', '丛书:': '幻象文库', 'ISBN:': ' 9787533957513', 'key': '沙德维尔的暗影', '出品方:': '理想国', '原作名:': ' Sherlock Holmes and the Shadwell Shadows'}
    e={'主标题': '黑色天鹅', ' 作者': '（日）鲇川哲也', '出版社:': ' 新星出版社', '副标题:': ' Shadwell Shadows', ' 译者': '王倩', '出版年:': ' 2019-11', '页数:': ' 432', '定价:': ' 49.00', '装帧:': ' 平装', '丛书:': '午夜文库·大师系列：鲇川哲也作品集', 'ISBN:': ' 9787513337816', 'key': '黑色天鹅', '出品方:': '理想国', '原作名:': ' 黒い白鳥'}

    reader=urlReader('https://book.douban.com/subject/34882702/')
    reader.start(caller)
    # T.insert(a)
    # T.insert(b)
    # T.insert(c)
    # T.insert(d)
    # T.insert(e)
    T.view()
    write2pk(T,'T.pk')
