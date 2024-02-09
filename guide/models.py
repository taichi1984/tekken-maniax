from django.db import models
from tekkenSite import settings
from ckeditor.fields import RichTextField


class Category(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.name


class Character(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    first_name_jp = models.CharField(max_length=50, default="")
    family_name_jp = models.CharField(max_length=50, default="")
    full_name_jp = models.CharField(max_length=50,default="")
    first_name_en = models.CharField(max_length=50, default="")
    family_name_en = models.CharField(max_length=50, default="")
    fighting_style = models.CharField(max_length=30)
    nationality = models.CharField(max_length=20)

    def __str__(self):
        return self.full_name_jp


# Create your models here.

class Guide(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default="")
    character = models.ForeignKey(Character, on_delete=models.CASCADE, default="")
    title = models.CharField(max_length=255)
    article = RichTextField()
    pub_date = models.DateTimeField('初回発行日',auto_now_add=True)
    update_date = models.DateTimeField('最終更新日')
    number_of_preview = models.BigIntegerField(default=0)
    publishing_setting = models.BooleanField(default=True)  # 公開設定　 1 = 全体公開 0 = 非公開
    is_deleted = models.BooleanField(default=False)  # 削除フラグ　True = 削除済み falee = 未削除

    def __str__(self):
        return self.title


class GuideComment(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE, default=None)
    contributor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    pub_date = models.DateTimeField('コメント投稿日')
    comment = models.TextField(default="")
    is_deleted = models.BooleanField(default="False")

    def __str__(self):
        return self.guide.title


class Evaluation(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE, default=None)
    evaluator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    evaluation = models.SmallIntegerField(default=0)  # 評価フラグ、0 =　無評価 , 1 = 高評価 , 2 = 低評価


class Favorite(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE, default=None)
