from operator import mod
from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.


User=get_user_model()
    

class Url(models.Model):
    long_url=models.CharField(max_length=1000)
    short_url=models.CharField(max_length=20,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    # user=models.ManyToManyField(User,related_name='urls')
    active=models.BooleanField(default=True)
    click_count=models.IntegerField(default=0)


    def __str__(self) -> str:
        return f"{self.long_url} > {self.short_url}"

    def increase_click_count(self):
        self.click_count+=1