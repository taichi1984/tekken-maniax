from django.db import models

# Create your models here.


class Tag(models.Model):
    id = models.AutoField(primary_key=True,auto_created=True)
    name = models.CharField(max_length=100,unique=True)

class Channel(models.Model):
    id = models.AutoField(primary_key=True,auto_created=True) #DB上のID
    channel_id = models.CharField(max_length=50,default="") #youtubeのチャンネルID
    update_playlist = models.CharField(max_length=50,default="") #youtubeチャンネルのUPLOAD動画のプレイリストのID
    latest_video_id = models.CharField(max_length=50,default="") #最新のアップロード動画のID
    is_broadcasting = models.BooleanField(help_text='配信中ならTrue',default=False) 
    channel_title = models.CharField(max_length=100,default="") #youtubeのチャンネル名
    description = models.TextField() #チャンネル説明文
    viewcount = models.IntegerField(default=0) #閲覧者数
    subscribercount = models.IntegerField(default=0) #登録者数
    videocount = models.IntegerField(default=0) #投稿動画数
    thumbnails_default = models.CharField(max_length=255,default="") #サムネイルのURL(def)
    thumbnails_medium = models.CharField(max_length=255,default="") #サムネイルのURL(mid)
    thumbnails_high = models.CharField(max_length=255,default="") #サムネイルのURL(high)
    live_broadcast_content = models.CharField(max_length = 100,default="") #配信コンテンツの有無
    publish_time = models.DateTimeField('チャンネル設立日') #チャンネル設立日
    tags = models.ManyToManyField(Tag, related_name ='channels',blank=True)

class Video(models.Model):
    id = models.AutoField(primary_key=True,auto_created=True) #DB上のID
    video_id = models.CharField(max_length=100,default="")
    title = models.CharField(max_length=100,default="")
    description = models.TextField()
    thumbnails_high = models.TextField(max_length=255)
    thumbnails_medium = models.TextField(max_length=255)
    thumbnails_default = models.TextField(max_length=255)
    channel_title = models.CharField(max_length=100,default="")
    playlist_id = models.CharField(max_length=100,default="")
    video_owner_channel_title = models.CharField(max_length=100,default="")
    video_owner_channel_id = models.CharField(max_length=100,default="")
    view_count = models.IntegerField(default=0)
    favorite_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    published_at = models.DateTimeField('動画投稿日',default='1990-01-01')
    tags = models.ManyToManyField(Tag, related_name ='videos',blank=True)