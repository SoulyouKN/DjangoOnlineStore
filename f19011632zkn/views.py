#coding=utf-8
import re

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from f19011632zkn.models import Goods,Address,Order,Orders,User
from f19011632zkn.forms import UserForm,LoginForm,AddressForm
from f19011632zkn.util import Util
import hashlib
# Create your views here.

# User Register
def register(request):
    if request.method == "POST":
        uf = UserForm(request.POST)
        if uf.is_valid():
            username = (request.POST.get('username')).strip()
            password = (request.POST.get('password')).strip()

            email = (request.POST.get('email')).strip()
            user_list = User.objects.filter(username=username)
            if user_list:
                uf = UserForm()
                return render(request,'register.html',{'uf':uf,"error":"User is exist yet!!!"})
            else:
                user = User()
                user.username = username
                user.password = password
                user.email = email
                user.save()
                uf = LoginForm()
                return render(request, 'index.html', {'uf':uf})
    else:
        uf = UserForm()
    return render(request,'register.html',{'uf':uf})

def index(request):
    uf = LoginForm()
    return render(request, 'index.html', {'uf':uf})

def login_action(request):
    if request.method == "POST":
        uf = LoginForm(request.POST)
        if uf.is_valid():
            username = (request.POST.get('username')).strip()
            password = (request.POST.get('password')).strip()
            if username =='' or password =='':
                return render(request,'index.html',{'uf':uf,"error":"NULL!!!"})
            else:
                user = User.objects.filter(username=username,password=password)
                if user:
                    responsed = HttpResponseRedirect('/goods_view/')
                    request.session['username'] = username
                    return  responsed
                else:
                    return render(request,'index.html',{'uf':uf,"error":"false username or password"})
    else:
        uf = LoginForm()
    return render(request,'index.html',{'uf':uf})

# Get User information
def user_info(request):
    #检查用户是否登录
    util = Util()
    username = util.check_user(request)
    #如果没有登录
    if username == "":
        uf = LoginForm()
        return render(request,"index.html",{'uf':uf,"error":"Please enter after login！"})
    else:
        #count为当前购物车中商品数量
        count = util.cookies_count(request)
        #获取用户登录信息
        user_list = get_object_or_404(User,username=username)
        #获取登录用户收货地址的所有信息
        address_list = Address.objects.filter(user_id=user_list.id)
        return render(request,"view_user.html",{"user":username,"user_info":user_list,"address":address_list,"count":count})

def change_password(request):
    util = Util()
    username = util.check_user(request)
    if username == "":
        uf = LoginForm()
        return render(request,"index.html",{'uf':uf,"error":"Please enter after Login!!!"})
    else:
        count = util.cookies_count(request)
        user_info = get_object_or_404(User,username = username)
        if request.method == "POST":
            oldpassword = util.md5((request.POST.get("oldpassword","")).strip())
            newpassword = util.md5((request.POST.get("newpassword", "")).strip())
            checkpassword = util.md5((request.POST.get("checkpassword", "")).strip())
            if oldpassword != user_info.password:
                return render(request,"change_password.html",{"user":username,"error":"Invalid Old Password！！","count":count})
            elif newpassword == oldpassword:
                return render(request, "change_password.html", {"user": username, "error": "Invalid Same Password！！", "count": count})
            elif newpassword !=checkpassword:
                return render(request, "change_password.html", {"user": username, "error": "Invalid Second Password！！", "count": count})
            else:
                User.objects.filter(username = username).update(password = newpassword)
                return render(request, "change_password.html", {"user": username, "error": "Successfully", "count": count})
        else:
            return render(request,"change_password.html", {"user": username,"count": count})

def logout(request):
    response = HttpResponseRedirect("/index/")
    del request.session['username']
    return response

def goods_view(request):
    # 检查用户是否登录
    util = Util()
    username = util.check_user(request)
    # 如果没有登录
    if username == "":
        uf = LoginForm()
        return render(request, "index.html", {'uf': uf, "error": "Please enter after login！"})
    else:
        # 获取所有商品信息
        good_list = Goods.objects.all()
        # count为当前购物车中商品数量
        count = util.cookies_count(request)

        paginator = Paginator(good_list,5)
        page = request.GET.get("page")
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        return render(request, "goods_view.html",
                      {"user": username, "goodss":contacts,"count": count})

def search_name(request):
    # 检查用户是否登录
    util = Util()
    username = util.check_user(request)
    # 如果没有登录
    if username == "":
        uf = LoginForm()
        return render(request, "index.html", {'uf': uf, "error": "Please enter after login！"})
    else:
        # count为当前购物车中商品数量
        count = util.cookies_count(request)
        search_name = (request.POST.get("good","")).strip()
        good_list = Goods.objects.filter(name__icontains=search_name)
        paginator = Paginator(good_list,5)
        page = request.GET.get("page")
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        return render(request, "goods_view.html",
                      {"user": username, "goodss":contacts,"count": count})

def view_goods(request,good_id):
    # 检查用户是否登录
    util = Util()
    username = util.check_user(request)
    # 如果没有登录
    if username == "":
        uf = LoginForm()
        return render(request, "index.html", {'uf': uf, "error": "Please enter after login！"})
    else:
        count = util.cookies_count(request)
        good = get_object_or_404(Goods,id = good_id)
        return render(request,'good_details.html',{"user":username,"good":good,"count":count})

def add_chart(request,good_id,sign):
    util = Util()
    username = util.check_user(request)
    # 如果没有登录
    if username == "":
        uf = LoginForm()
        return render(request, "index.html", {'uf': uf, "error": "Please enter after login！"})
    else:
        good = get_object_or_404(Goods, id=good_id)
        if sign == "1":
            response = HttpResponseRedirect("/goods_view/")
        else:
            response = HttpResponseRedirect("/view_goods/"+good_id)
        response.set_cookie(str(good.id),1,60*60*24*365)
        return response

def view_chart(request):
    # 检查用户是否登录
    util = Util()
    username = util.check_user(request)
    # 如果没有登录
    if username == "":
        uf = LoginForm()
        return render(request, "index.html", {'uf': uf, "error": "Please enter after login！"})
    else:
        count = util.cookies_count(request)
        print("++++++++++++++++++")
        print(count)
        my_chart_list = util.add_chart(request)
        return render(request,'view_chart.html',{"user":username,"goodss":my_chart_list,"count":count})

def update_chart(request,good_id):
    # 检查用户是否登录
    util = Util()
    username = util.check_user(request)
    # 如果没有登录
    if username == "":
        uf = LoginForm()
        return render(request, "index.html", {'uf': uf, "error": "Please enter after login！"})
    else:
        good = get_object_or_404(Goods,id = good_id)
        count = (request.POST.get("count"+good_id,"")).strip()
        if int(count)<=0:
            my_chart_list = util.add_chart(request)
            return render(request,"view_chart.html",{"user":username,"goodss":my_chart_list,"error":"个数不能小于等于0"})
        else:
            response = HttpResponseRedirect("/view_chart")
            response.set_cookie(str(good.id),count,60*60*24*365)
            return response


def remove_chart(request,good_id):
    # 检查用户是否登录
    util = Util()
    username = util.check_user(request)
    # 如果没有登录
    if username == "":
        uf = LoginForm()
        return render(request, "index.html", {'uf': uf, "error": "Please enter after login！"})
    else:
        good = get_object_or_404(Goods,id = good_id)
        response = HttpResponseRedirect("/view_chart")
        response.set_cookie(str(good.id),1,0)
        return response

def remove_chart_all(request):
    # 检查用户是否登录
    util = Util()
    username = util.check_user(request)
    # 如果没有登录
    if username == "":
        uf = LoginForm()
        return render(request, "index.html", {'uf': uf, "error": "Please enter after login！"})
    else:
        response = HttpResponseRedirect("/view_chart/")
        cookie_list = util.deal_cookies(request)
        for key in cookie_list:
            response.set_cookie(str(key),1,0)
        return response

def view_address(request):
    # 检查用户是否登录
    util = Util()
    username = util.check_user(request)
    # 如果没有登录
    if username == "":
        uf = LoginForm()
        return render(request, "index.html", {'uf': uf, "error": "Please enter after login！"})
    else:
        user_list = get_object_or_404(User,username = username)
        address_list = Address.objects.filter(user_id = user_list.id)
        return render(request,"view_address.html",{"user":username,"addresses":address_list})

def add_address(request,sign):
    # 检查用户是否登录
    util = Util()
    username = util.check_user(request)
    # 如果没有登录
    if username == "":
        uf = LoginForm()
        return render(request, "index.html", {'uf': uf, "error": "Please enter after login！"})
    else:
        user_list = get_object_or_404(User,username = username)
        address_list = Address.objects.filter(user_id = user_list.id)
        return render(request,"view_address.html",{"user":username,"addresses":address_list})