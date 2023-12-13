from django.core.management.base import BaseCommand
from video.util.youtube_video_getter import search_channel_list,get_channel_info_from_channelids
from video.models import Channel
import json

class Command(BaseCommand):
    help = 'Describe what the command does here'

    def handle(self, *args, **options):
        #channels = search_channel_list("鉄拳8") #本番用 APIからデータ取得
        #with open("data.json", "w") as file:
        #   json.dump(channels,file)
        
        with open("data.json","r") as file:
            channels = json.load(file)

        for channel in channels:
            Channel.objects.update_or_create(
            channel_id = channel["snippet"]["channelId"],
            defaults={
               'channel_title' : channel["snippet"]["channelTitle"],
               'description' : channel["snippet"]["description"],
               'thumbnails_default' : channel["snippet"]["thumbnails"]["default"]["url"],
               'thumbnails_medium' :channel["snippet"]["thumbnails"]["medium"]["url"],
               'thumbnails_high' : channel["snippet"]["thumbnails"]["high"]["url"],
               'publish_time' : channel["snippet"]["publishTime"]    
            }
        )
        
        all_channels = Channel.objects.all()
        i = 0
        channel_ids = []
        channels_info =[]
        channels_data = []
        for channel in all_channels:

            if i < 49:
                channel_ids.append(channel.channel_id)
                i +=1
            else:
                channels_info = get_channel_info_from_channelids(channel_ids)
                for channel_data in channels_info["items"]:
                    channels_data.append(channel_data)

                channel_ids = []
                channels_info =[]
                i = 0
        
        #あまり分の処理をもう１回だけ同じことをやる。
        channels_info = get_channel_info_from_channelids(channel_ids)
        for channel_data in channels_info["items"]:
            channels_data.append(channel_data)

   
        for channel in channels_data:
            Channel.objects.update_or_create(
                channel_id = channel["id"],
                defaults = {
                    "viewcount":int(channel["statistics"]["viewCount"]),
                    "update_playlist":channel["contentDetails"]["relatedPlaylists"]["uploads"],
                    "subscribercount" : int(channel["statistics"]["subscriberCount"]),
                    "videocount" : int(channel["statistics"]["videoCount"])
                }
            )          

        self.stdout.write('Batch process has been executed')

   