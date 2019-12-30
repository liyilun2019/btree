class Tnode:
    def __init__(self,idx,maxcnt,isleave):
        self.maxcnt=maxcnt
        self.spliter=[]
        self.isleave=isleave
        self.children=[]
        self.idx=idx
        self.fa=None

    def search(self,key):
        if self.isleave and len(self.spliter)==0:
            return {'ret':self,'kind':'empty'}
        if self.isleave:
            for ind,s in enumerate(self.spliter):
                if(s==key):
                    return {'ret':self.children[ind],'kind':'Lnode'}
                if(key<s):
                    return {'ret':self,'kind':'hasright','right':self.children[ind]}
            return {'ret':self,'kind':'hasleft','left':self.children[-1]}

        for ind,s in enumerate(self.spliter):
            if(key<=s):
                return self.children[ind].search(key)
        return self.children[-1].search(key)

    def insert(self,key,cnd,tree):
        ind = len(self.spliter)
        for i in range(len(self.spliter)):
            if self.spliter[i]>key:
                ind=i
                break
        self.spliter.insert(ind,key)
        if self.isleave:
            self.children.insert(ind,cnd)
        else:
            self.children.insert(ind+1,cnd)
        if(len(self.spliter)>self.maxcnt):
            self.split(tree)

    def split(self,tree):
        fa=self.fa
        newtnd_r=tree.newTnd(True)
        if(fa==None):
            fa=tree.newTnd(False)
            fa.children.append(self)
            tree.treert=fa
        self.fa=fa
        mid=len(self.spliter)//2
        for i in range(mid+1,len(self.spliter)):
            newtnd_r.insert(self.spliter[i],self.children[i],tree)
        newsp,newch=[],[]
        for i in range(0,mid+1):
            newsp.append(self.spliter[i])
            newch.append(self.children[i])
        fa.insert(self.spliter[mid],newtnd_r,tree)
        self.spliter=newsp
        self.children=newch

    def __str__(self):
        return str({'idx':self.idx,'spliter':self.spliter,'children':[str(c) for c in self.children],'isleave':self.isleave})

class Lnode:
    def __init__(self,idx,obj,prev,nxt):
        self.idx=idx
        self.obj=obj
        self.prev=prev
        self.nxt=nxt

    def __str__(self):
        if(self.obj==None):
            return 'None'
        return str({'obj':self.obj['key']})

class Tree:
    def __init__(self,maxcnt):
        self.maxcnt=maxcnt
        self.nodespace=[Tnode(0,maxcnt,True)]
        head=Lnode(0,None,None,None)
        tail=Lnode(0,None,None,None)
        head.nxt=tail
        tail.prev=head
        self.lndspace=[head,tail]

        self.listrt=self.lndspace[0]
        self.treert=self.nodespace[0]

    def newTnd(self,isleave):
        newtnd=Tnode(len(self.nodespace),self.maxcnt,isleave)
        self.nodespace.append(newtnd)
        return newtnd

    def search(self,key):
        return self.treert.search(key)

    def insert(self,obj):
        obj=obj.copy()
        key=obj['key']
        retdic=self.search(key)
        if(retdic['kind']=='Lnode'):
            print(f'dumplicated key: {key}')
            return False
        newlnd=None
        if(retdic['kind']=='hasright'):
            newlnd=self.insert_link_l(obj,retdic['right'])
        elif(retdic['kind']=='hasleft'):
            newlnd=self.insert_link_r(obj,retdic['left'])
        else:
            newlnd=self.insert_link_r(obj,self.listrt)

        retdic['ret'].insert(key,newlnd,self)
        return True
    
    def insert_link_l(self,obj,right):
        newLnode=Lnode(len(self.lndspace),obj,right.prev,right)
        right.prev.nxt=newLnode
        right.prev=newLnode
        self.lndspace.append(newLnode)
        return newLnode

    def insert_link_r(self,obj,left):
        newLnode=Lnode(len(self.lndspace),obj,left,left.nxt)
        left.nxt.prev=newLnode
        left.nxt=newLnode
        self.lndspace.append(newLnode)
        return newLnode

    def view(self):
        print(self.treert)
        l=self.listrt
        while l.nxt!=None:
            print(l)
            l=l.nxt


