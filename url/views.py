from distutils.log import error
from telnetlib import STATUS
from django.forms import ValidationError
from django.urls import reverse
from django.conf import settings
from django.shortcuts import redirect, render,get_object_or_404
from .models import Url
import string,random
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from .forms  import UrlForm
import sys
import datetime
from django.core.validators import URLValidator
URLValidator()


def update_click_count(request,pk):    
    obj=get_object_or_404(Url,short_url=pk)
    obj.increase_click_count()
    obj.save()


def redirect_target_url(request,pk):
    context={}
    url_obj=get_object_or_404(Url,short_url=pk)
    # return render(request,'urls/a.html',context)
    update_click_count(request,pk)
    return redirect(url_obj.long_url)


def validate_url(request,url):
    print('this is validate_url_func')
    try:
        print('this is try')
        URLValidator()(url)
    except  ValidationError as e:
        print('this is exception')
        raise HttpResponseBadRequest('enter a valid url')
        # return HttpResponseRedirect(reverse('url:create_short_url'),status=302)
    # return render(request,'urls/index.html')
    return redirect(reverse('url:create_short_url'))


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
            # validate_url(request,_long_url)
            if Url.objects.filter(long_url=_long_url).exists():
                obj=get_object_or_404(Url,long_url=_long_url)
                return HttpResponse(domain+obj.short_url)
            else:
                slug=''
                for i in range(5):
                    slug +=random.choice(string.ascii_letters)
                short_url=slug
                # long_url = form.cleaned_data["long_url"]
                # print(f"long_url:{long_url}")
                new_url = Url(long_url=_long_url, short_url=slug)
                new_url.save()
                # context['short_url']=domain+slug
                # request.user.urlshort.add(new_url)
                # return redirect_url(request,short_url)
                # return JsonResponse({"long_url":long_url,"short_url":domain+slug})
                # return redirect(reverse("url:a",kwargs={"secret_key":slug}))
                return HttpResponse(domain+slug)
        return HttpResponse(form.error)   
    else:
        form = UrlForm()
    # data = UrlData.objects.all()
    context['form']=form
    return render(request, 'urls/index.html', context)


def register(request):
    pass

