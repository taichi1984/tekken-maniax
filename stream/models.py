from django.db import models

# Create your models here.

class Platform(models.Model):
    id = models.AutoField(primary_key=True,auto_created=True) #DB上のID
    name = models.CharField(max_length=50,default="") #platform名,Youtube,twitchなど



class Stream(models.Model):
    id = models.AutoField(primary_key=True,auto_created=True) #DB上のID
    platform = models.ForeignKey(Platform,on_delete=models.CASCADE)
    title = models.CharField(max_length=255,default="")
    user_name = models.CharField(max_length=255,default="")
    viewer_count = models.IntegerField(default=0)
