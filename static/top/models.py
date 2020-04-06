from django.db import models
from guide.models import Character
from django.contrib.auth.models import AbstractUser

from tekkenSite import settings


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True,default="")


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nick_name = models.CharField(max_length=50, default="")
    main_character = models.ForeignKey(Character, on_delete=models.CASCADE, default=1)
    introduction = models.TextField(default="")
    is_deleted = models.BooleanField(default=False)
