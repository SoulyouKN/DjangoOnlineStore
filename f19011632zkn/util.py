#coding:utf-8
# from xml.dom import minidom
from django.shortcuts import render,get_object_or_404
from f19011632zkn.models import Goods,Address,Order,Orders,User
from f19011632zkn.object import Chart_list,Order_list,Orders_lsit
import hashlib

class Util:
    def check_user(self,request):
        username = str(request.session.get('username',''))
        user = User.objects.filter(username =username)
        if(user is None):
            return ""
        else:
            return username

    def is_number(self,s):
        try:
            int(s)
            return True
        except ValueError:
            pass
        return False

    def cookies_count(self,request):
        cookie_list = request.COOKIES
        length = 0
        for i in cookie_list:
            if(self.is_number(i)):
                length = length + 1
        return length

    def add_chart(self,request):
        cookie_list = self.deal_cookies(request)
        my_chart_list = []
        for key in cookie_list:
            chart_object = Chart_list
            chart_object = self.set_chart_list(key,cookie_list)
            my_chart_list.append(chart_object)
        return my_chart_list

    # def cookies_count(self, request):
    #     cookie_list = request.COOKIES
    #     if "csrftoken" in cookie_list:
    #         return len(requests.COOKIES) - 2
    #     else:
    #         return len(requests.COOKIES) - 1

    def deal_cookies(self, request):
        cookie_list = request.COOKIES
        cookie_list.pop("sessionid")
        if "csrftoken" in cookie_list:
            cookie_list.pop("csrftoken")
        return cookie_list

    def set_chart_list(self,key,cookie_list):
        chart_list = Chart_list()
        good_list = get_object_or_404(Goods,id=key)
        chart_list.set_id(key)
        chart_list.set_name(good_list.name)
        chart_list.set_price(good_list.price)
        chart_list.set_count(cookie_list[key])
        return chart_list

# class GetXML:
#     def __init__(self,myXmlFile):
#         dom = minidom.parse(myXmlfile)
#         self.root = dom.documentElement
#     def getxmldata(xmlfile):
#     #从XML中读取数据
#         TestIds = self.root.getElementsByTagName('TestId')
#         Titles = self.root.getElementsByTagName('Title')
#         Methods = self.root.getElementsByTagName('Method')
#         Deses = self.root.getElementsByTagName('Desc')
#         Urls = self.root.getElementsByTagName('Url')
#         InptArgs = self.root.getElementsByTagName('InptArg')
#         Results = self.root.getElementsByTagName('Result')
#         CheckWords = selfroot.getElementsByTagName('CheckWord')
#         i=0
#         mylists=[]
#         for TestId in TestIds:
#             mydicts={}
#             #获取每个数据,形成字典
#             mydicts ["TestId"] = (TestIds[i].firstchild.data).strip()
#             mydicts["Title"] =(Titles[i].firstchild.data).strip()
#             mydicts ["Method"]=(Methods[i].firstChild.data).strip()
#             mydictst["Desc"]=(Descs[i].firstChild.data).strip()
#             mydicts ["Url"] =(Uris[i].firstChild.data).strip()
#             if((InptArgs[i].firstChild)is None):
#                 mydicts [ "InptArg"]=""
#             else:
#                 mydicts["InptArg"] =(InptArgs[i].firstChild.data).strip()
#             mydicts ["Result"] =(Results[i].firstChild.data).strip()
#             mydicts["CheckWord"] = (CheckWords[i].firstChild.data).strip()
#             mylists.append(mydicts)
#             i = i + 1
#         return mylists
#
#     def getUserInitInfo(self):
#         id = self.root.getElementsByTagName('id')
#         id = (str(id[0].firstChild.data)).strip()
