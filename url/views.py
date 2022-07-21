import string,random
from datetime import datetime
from time import perf_counter
from xmlrpc.client import DateTime
from django.forms import ValidationError
from django.urls import reverse
from django.conf import settings
from django.shortcuts import redirect, render,get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.validators import URLValidator
from django.contrib.auth import login as _login, authenticate, logout as _logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Info, Url,User
from .forms  import UrlForm,RegisterForm,LoginForm


def update_click_count(request,pk):    
    obj=get_object_or_404(Url,short_url=pk)
    obj.increase_click_count()
    obj.save()


# @staticmethod
# def runtime_calculator(func):
#     def wrapper(*args,**kwargs):
#         start_runtime=perf_counter()
#         func(*args,**kwargs)
#         end_runtime=perf_counter
#         runtime=end_runtime-start_runtime
#         return runtime
#     return func
        

def redirect_target_url(request,pk):
    context={}
    url_obj=get_object_or_404(Url,short_url=pk)
    if request.user.is_authenticated:
        print(request.user.username)
        print(type(request.user.username))
    else:
        print(request.user)
        print(type(request.user))
    update_click_count(request,pk)
    return redirect(url_obj.long_url)


@login_required(login_url='login/')
def create_short_url(request):
    context={}
    domain="http://localhost:8000/"
    if request.method == 'POST':
        start_response_time=perf_counter()
        form = UrlForm(request.POST)
        if form.is_valid():
            _long_url=form.cleaned_data['long_url']
            try:
             URLValidator()(_long_url)
            except  ValidationError:
                return HttpResponseBadRequest('Enter a valid url')
            _usr_obj=request.user
            if Url.objects.filter(long_url=_long_url).exists():# User enter a repetitive long link
                obj_url=get_object_or_404(Url,long_url=_long_url)
                _short_url=obj_url.short_url
            else:# User enter a new long link
                _short_url=''
                for i in range(5):
                    _short_url +=random.choice(string.ascii_letters)
                obj_url = Url.objects.create(long_url=_long_url, short_url=_short_url)
            obj_url.user.add(_usr_obj)
            try:
                info_obj=Info.objects.get(Q(user=_usr_obj.id),Q(url=obj_url.id))
                info_obj.created_at=datetime.now()
                info_obj.save()
            except Exception as e:
                return HttpResponse(e)
            end_response_time=perf_counter()
            _response_time=end_response_time-start_response_time
            info_obj.response_time=_response_time
            info_obj.save()
            return HttpResponse(domain+_short_url)
        return HttpResponse(form.errors)   
    else:
        form = UrlForm()
        context['form']=form
    return render(request, 'urls/index.html', context)


def register(request):
    context={}
    if request.method=='POST':
            form=RegisterForm(request.POST)
            if form.is_valid():
                _username=form.cleaned_data.get('username','')
                if User.objects.filter(username=_username).exists():
                    return render(request,'urls/register.html',{"error":"username already exist"})
                else:
                    form.save()
                    get_object_or_404
                    return render(request,'urls/register.html',{"form":form,"msg":"user created sucessfully"})
            else:
                return HttpResponse(form.errors)
    else:
        form=RegisterForm()
        context['form']=form
        return render(request,'urls/register.html',context)
    

def login(request):
    context={}
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            _username = form.cleaned_data.get("username", "")
            _password = form.cleaned_data.get("password", "")
            user = authenticate(request, username=_username, password=_password)
            if user:
                _login(request, user)
                return redirect('url:create_short_url')
            else :
                return HttpResponse('please enter your username and password correctly')
        else:
            return HttpResponse(form.errors)
    else:
        form=LoginForm()
        context['form']=form
        return render(request,'urls/login.html',context)        


def logout(request):
    form = UrlForm()
    context={"form":form,"msg":"you loged out"}
    _logout(request)
    return render(request,'urls/index.html',context)


def user_statics(request,pk):# each user can see it
    context={}
    info_list=Info.objects.filter(user=pk)
    context['info_list']=info_list
    return render(request,'urls/statics.html',context)

def analysis(request):# Only superusers can see it
    pass