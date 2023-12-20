from django.core.management.base import BaseCommand
from video.util.youtube_video_getter import get_latest_video_id_by_channel_ids,get_broadcasting_status_by_video_ids
from video.models import Channel
import json
import redis

class Command(BaseCommand):
    help = 'Describe what the command does here'

    def handle(self, *args, **options):
        
        channels = Channel.objects.all()
        channel_ids = []
        for channel in channels:
            channel_ids.append(channel.channel_id)

        video_id_list = get_latest_video_id_by_channel_ids(channel_ids)
        
        '''
        #DBに最新の動画情報を保存する。redisでやるのでいったんコメントアウト
        for video_id in video_id_list:
            channel = Channel.objects.filter(channel_id = video_id["channel_id"]).get()
            channel.latest_video_id = video_id["video_id"]
            channel.save()
        '''

        video_ids = []
        for video_id in video_id_list:
            video_ids.append(video_id['video_id'])

        broadcasting_status_list = get_broadcasting_status_by_video_ids(video_ids)


        for broadcast_status in broadcasting_status_list:
            if broadcast_status["liveBroadcastContent"] == "live":
                print(f'video id : { broadcast_status["video_id"] }' + " is livestreaming " )
                print(broadcast_status.keys())


    
        self.stdout.write('Batch process has been executed')

   