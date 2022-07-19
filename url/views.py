from django.conf import settings
from django.shortcuts import redirect, render,get_object_or_404
from .models import Url
import string,random
from django.http import HttpResponse
from .forms  import UrlForm
import sys


def redirect_url(request,url):
    url_obj=get_object_or_404(Url,short_url=url)
    return redirect(url_obj.long_url)


def create_short_url(request):
    context={}
    domain="http://localhost:8000/"
    if request.method == 'POST':
        form = UrlForm(request.POST)
        if form.is_valid():
            slug=''
            for i in range(10):
                slug +=random.choice(string.ascii_letters)
            short_url=slug
            long_url = form.cleaned_data["long_url"]
            print(f"long_url:{long_url}")
            new_url = Url(long_url=long_url, short_url=short_url)
            new_url.save()
            # request.user.urlshort.add(new_url)
            return redirect_url(request,short_url)
            
    else:
        form = UrlForm()
    # data = UrlData.objects.all()
    context['form']=form
    return render(request, 'urls/url.html', context)


def register(request):
    pass

