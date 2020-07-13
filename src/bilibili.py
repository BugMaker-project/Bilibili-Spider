import random
import requests
import numpy as np
import lxml.etree
import os
import threading
v1 = None
v2 = None
v3 = None
v4 = None
v5 = None
v6 = None
v7 = None
v8 = None
v9 = None
class UserSetting(object):
    """用户设定的解析器。"""
    def __init__(self):
        self.setting="setting.xml"
        self.content=lxml.etree.parse(self.setting)
        self.icon=None
        self.code=None
        self.code1=None
        self.code2=None
        self.urlMode=None
        self.mirror=None
        self.getInfo()
    def getInfo(self):
        root=self.content.getroot()
        for article in root:
            for field in article:
                if field.tag=="code":
                    self.code=field.text
                elif field.tag=="code1":
                    self.code1 = field.text
                elif field.tag=="code2":
                    self.code2 = field.text
                if field.tag=="parameter":
                    for element in field:
                        if element.tag=="avbv":
                            self.urlMode=element.text
                        if element.tag=="favicon":
                            self.icon=element.text
    def isRealVersion(self):
        if Var.code[0]==self.code:
            if Var.code[1]==self.code1:
                if Var.code[2]==self.code2:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
class Spider(object):
    """爬json的类"""
    def __init__(self,bv:str):
        self.bv=bv.replace("bv","").replace("BV","").replace("Bv","").replace("bV","")
        self.url=(Var.bilibiliVideoApi+bv)
        self.headers={
            "User-Agent":random.choice(Var.USER_AGENT_LIST),
            "Referer": "https://www.bilibili.com",
            }
    def updateHeader(self)->None:
        self.headers["User-Agent"]=random.choice(Var.USER_AGENT_LIST)
    def get(self,flag:int=0,url:str=None):
        if flag==0:
            reponse=requests.get(self.url,headers=self.headers)
        elif flag==1:
            reponse=requests.get(url,headers=self.headers)
        else:
            raise ValueError("The flag is wrong.")
        return reponse
class Parser(object):
    """解析器类。解析json文件并提取数据。"""
    def __init__(self,spider:Spider):
        self.spider=spider
        self.reponse=self.spider.get()
        self.content=self.reponse.json()
    def jsonParser(self):
        Title=self.content["data"]["title"]#标题
        aid=self.content["data"]["aid"]#AV号
        bvid=self.content["data"]["bvid"]#BV号
        View=self.content["data"]["stat"]["view"]#观看量
        Favourite=self.content["data"]["stat"]["favorite"]#收藏
        Coin=self.content["data"]["stat"]["coin"]#硬币
        Share=self.content["data"]["stat"]["share"]#分享
        Like=self.content["data"]["stat"]["like"]#赞
        return {
            "title":Title,
            "aid":aid,
            "bvid":bvid,
            "view":View,
            "favourite":Favourite,
            "coin":Coin,
            "share":Share,
            "like":Like
            }
class Video(object):
    """视频Data Object.储存视频的底层方法
    在子类Bilibili中定义其他方法。"""
    def __init__(self,bv:str):
        self.bv=bv
        self.url=(Var.bilibiliVideoApi+bv)
        self.spider=Spider(self.bv)
        self.parser=Parser(self.spider)
        self.data=self.parser.jsonParser()
        self.title=self.data["title"]
        self.aid=self.data["aid"]
        self.bvid=self.data["bvid"]
        self.view=self.data["view"]
        self.favourite=self.data["favourite"]
        self.coin=self.data["coin"]
        self.share=self.data["share"]
        self.like=self.data["like"]
        self.line=8
        self.gc()
    def gc(self):
        del self.bv,self.url,self.spider,self.parser,self.data
    def avidGet(self):
        return self.aid
    def __str__(self):
        return "标题:\n%s;\nav:av%d;\nbv:%s;\n观看人数:%d;\n收藏人数:%d;\n硬币数量:%d;\n分享数量:%d;\n点赞数量:%d\n%s分界线君%s\n"\
              %(self.title,self.aid,self.bvid,self.view,self.favourite,self.coin,self.share,self.like,"-"*self.line,"-"*self.line)
    def str(self):
        return "av:av%d;\nbv:%s;\n观看人数:%d;\n收藏人数:%d;\n硬币数量:%d;\n分享数量:%d;\n点赞数量:%d\n%s分界线君%s\n"\
              %(self.aid,self.bvid,self.view,self.favourite,self.coin,self.share,self.like,"-"*self.line,"-"*self.line)
class Bilibili(Video):
    """Video的子类，补充他的的一些操作。"""
    def __init__(self,setting:UserSetting,bv:str):
        Video.__init__(self,bv)
        if setting.urlMode=="bvid":
            self.link=self.urlget()["Bvid_Version"]
        elif setting.urlMode=="aid":
            self.link=self.urlget()["Aid_Version"]
    def isYingXiaoHao(self):
        if self.view<=400:
            return False
        if self.like>=50000:
            return False
        if self.like/self.view<=Var.list_view:
            return True

    def urlget(self):
        return {
            "Aid_Version":"https://www.bilibili.com/video/av"+str(self.aid),
            "Bvid_Version":"https://www.bilibili.com/video/"+self.bvid
        }
class Var():
    USER_AGENT_LIST=[
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
    flag_zan_and_view=False
    list_view=0
    setting = UserSetting()
    bilibiliVideoApi="https://api.bilibili.com/x/web-interface/view?bvid="
    code=["DpiDUQRvIb03UpvITy36129zFhfvRnSxQGsomASa",
         "HpMWRSiFUHghhKzkOXU7n1f7vkL58V4yzl3xn6M5",
         "DsSa9iSlRLyoRzlKINuYCJV5P6znhZIEk0yai8M0"]
    @classmethod
    def Average(cls,arr:list) -> int:
        return sum(arr)/len(arr)
    @classmethod
    def v1Return(cls):
        global v1
        v1 = Bilibili(cls.setting, "BV1Eg4y1v7WY")
    @classmethod
    def v2Return(cls):
        global v2
        v2 = Bilibili(cls.setting, "BV1Eg4y1v7WY")
    @classmethod
    def v3Return(cls):
        global v3
        v3 = Bilibili(cls.setting, "BV1554y1q7AT")
    @classmethod
    def v4Return(cls):
        global v4
        v4 = Bilibili(cls.setting, "BV1554y1q7AT")
    @classmethod
    def v5Return(cls):
        global v5
        v5 = Bilibili(cls.setting, "BV1ep4y1U7VG")
    @classmethod
    def v6Return(cls):
        global v6
        v6 = Bilibili(cls.setting, "BV11V41167cQ")
    @classmethod
    def v7Return(cls):
        global v7
        v7 = Bilibili(cls.setting, "BV1qt411J7Jn")
    @classmethod
    def v8Return(cls):
        global v8
        v8 = Bilibili(cls.setting, "BV1ex411d7o5")
    @classmethod
    def v9Return(cls):
        global v9
        v9 = Bilibili(cls.setting, "BV1b7411n7uR")
    @classmethod
    def like_and_view(cls):
        if cls.flag_zan_and_view==False:
            global v1, v2, v3, v4, v5, v6, v7, v8, v9
            def gc():
                global v1,v2,v3,v4,v5,v6,v7,v8,v9
                del v1,v2,v3,v4,v5,v6,v7,v8,v9,
            v1t=threading.Thread(target=cls.v1Return)
            v2t=threading.Thread(target=cls.v2Return)
            v3t=threading.Thread(target=cls.v3Return)
            v4t=threading.Thread(target=cls.v4Return)
            v5t=threading.Thread(target=cls.v5Return)
            v6t=threading.Thread(target=cls.v6Return)
            v7t=threading.Thread(target=cls.v7Return)
            v8t=threading.Thread(target=cls.v8Return)
            v9t=threading.Thread(target=cls.v9Return)
            v1t.run()
            v2t.run()
            v3t.run()
            v4t.run()
            v5t.run()
            v6t.run()
            v7t.run()
            v8t.run()
            v9t.run()
            like_and_view= [[v1.like,v1.view],[v2.like,v2.view],[v3.like,v3.view],
                            [v4.like,v4.view],[v5.like,v5.view],[v6.like,v6.view],
                            [v7.like,v7.view],[v8.like,v8.view],[v9.like,v9.view]
                       ]
            print(like_and_view)
            list_like_view=[]
            for v in like_and_view:
                list_like_view.append(v[0]/v[1])
            for index_v in range(len(list_like_view)):
                list_like_view[index_v]=round(list_like_view[index_v],4)
            cls.list_view=round(cls.Average(list_like_view),4)
            cls.flag_zan_and_view=True
            gc()
            del v1t,v2t,v3t,v4t,v5t,v6t,v7t,v8t,v9t
        else:
            cls.list_view=cls.list_view

def test():
    setting=UserSetting()
    Var.like_and_view()
    print(Var.list_view)
    print(Bilibili(setting=setting,bv="BV1oV411C7cx").isYingXiaoHao())

if __name__=="__main__":
    test()