from django.core.cache import cache
from django.core.management.base import BaseCommand
from video.util.youtube_video_getter import get_latest_video_id_by_channel_ids,get_broadcasting_status_by_video_ids
from video.models import Channel
import requests
import json
import redis

class Command(BaseCommand):
    help = 'Describe what the command does here'
    def handle(self, *args, **options):
        #cache.set("keyA","value2")        
        r = redis.Redis(host='localhost',port=6379,db=1)
        value = r.hgetall("live_stream:test2")
        print(value)

        self.stdout.write('Batch process has been executed')

   