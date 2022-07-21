import string,random
from django.forms import ValidationError
from django.urls import reverse
from django.conf import settings
from django.shortcuts import redirect, render,get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.validators import URLValidator
from django.contrib.auth import login as _login, authenticate, logout as _logout
from .models import Url,User
from .forms  import UrlForm,RegisterForm,LoginForm


def update_click_count(request,pk):    
    obj=get_object_or_404(Url,short_url=pk)
    obj.increase_click_count()
    obj.save()


def redirect_target_url(request,pk):
    context={}
    url_obj=get_object_or_404(Url,short_url=pk)
    update_click_count(request,pk)
    return redirect(url_obj.long_url)


def create_short_url(request):
    context={}
    domain="http://localhost:8000/"
    if request.method == 'POST':
        form = UrlForm(request.POST)
        if form.is_valid():
            _long_url=form.cleaned_data['long_url']
            try:
             URLValidator()(_long_url)
            except  ValidationError:
                return HttpResponseBadRequest('Enter a valid url')
            if Url.objects.filter(long_url=_long_url).exists():
                obj=get_object_or_404(Url,long_url=_long_url)
                return HttpResponse(domain+obj.short_url)
            else:
                slug=''
                for i in range(5):
                    slug +=random.choice(string.ascii_letters)
                short_url=slug
                new_url = Url(long_url=_long_url, short_url=slug)
                new_url.save()
                return HttpResponse(domain+slug)
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
            _username = request.POST.get("username", "")
            _password = request.POST.get("password", "")
            user = authenticate(request, username=_username, password=_password)
            if user is not None:
                _login(request, user)
                return render(request,'urls/login.html',{"form":form,"msg":"you loged in successfuly"})        
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


def user_static():
    pass

