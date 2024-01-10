from django.core.management.base import BaseCommand
from video.util.youtube_video_getter import get_latest_video_id_by_channel_ids,get_broadcasting_status_by_video_ids
from video.models import Channel
from stream.util.UpdateStreamingData import UpdateTwitchStreamingInfo,UpdateYoutubeStreamingInfo
import json
import redis

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        red = redis.Redis(host='localhost',port=6379,db=1)

        help = 'Describe what the command does here'
        count = UpdateTwitchStreamingInfo(0)
        print("t_count : " + str(count))
        count = UpdateYoutubeStreamingInfo(count)
        print("y_count : " + str(count))
        red.set('stream_count',count)

        
    
        self.stdout.write('Batch process has been executed')

