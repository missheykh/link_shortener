from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.


User=get_user_model()
    

class Url(models.Model):
    long_url=models.CharField(max_length=1000)
    short_url=models.CharField(max_length=20,null=True,blank=True)
    user=models.ManyToManyField(User,related_name='urls',through='Info')
    active=models.BooleanField(default=True)
    click_count=models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.long_url} > {self.short_url}"

    def increase_click_count(self):
        self.click_count+=1


class Info(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,related_name='urlinfo',null=True)
    url=models.ForeignKey(Url,on_delete=models.CASCADE,related_name='linkinfo')
    created_at=models.DateTimeField(null=True,blank=True)
    response_time=models.FloatField(null=True)
    os=models.CharField(max_length=40,null=True)

    def __str__(self) -> str:
        return f"{self.user.username} > {self.url.long_url}"