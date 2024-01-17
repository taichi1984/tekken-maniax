from django.db import models
from guide.models import Character
from django.contrib.auth.models import AbstractUser
from tekkenSite import settings


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, default="")



# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nick_name = models.CharField(max_length=50, default="")
    main_character = models.ForeignKey(Character, on_delete=models.CASCADE, default=1)
    twitter_account = models.CharField(max_length=60, default="")
    youtube_channel_url = models.CharField(max_length=60, default="")
    twitch_url = models.CharField(max_length=255, default="")
    introduction = models.TextField(default="")
    is_deleted = models.BooleanField(default=False)


# notification
class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    notification_text = models.CharField(max_length=255, default="")
    alreadyRead = models.BooleanField(default=False)
    pub_date = models.DateTimeField('通知日')


class ChangeLog(models.Model):
    pub_date = models.DateTimeField('更新日')
    log = models.TextField(default="")
    
    def __str__(self):
        return self.pub_date


