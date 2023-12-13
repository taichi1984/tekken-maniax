from django.core.management.base import BaseCommand
from video.models import Channel,Video
from video.util.youtube_video_getter import get_video_info_by_channel , get_video_statistics_info_by_videoids
import json

class Command(BaseCommand):
    help = 'Description of your command'

    def add_arguments(self, parser):
        # コマンドライン引数をここで定義
        pass

    def handle(self, *args, **options):

        #
        # チャンネルデータをもとに各チャンネルの最新20件の動画データを取得する処理
        #

        '''
        channels = Channel.objects.all()
        videos = []
        for channel in channels:
            videos.append(get_video_info_by_channel(channel.channel_id))
        
        with open("videodata.json","w") as file:
            json.dump(videos,file)
        '''
        
        with open("videodata.json","r") as file:
            videos = json.load(file)
        i = 0 
        '''
        for video in videos :
            if isinstance(video, dict):
                  for item in video["items"] :
                      
                      Video.objects.update_or_create(
                          video_id = item["snippet"]["resourceId"]["videoId"],
                          defaults={
                            'title' : item["snippet"]["title"],
                            'description' : item["snippet"]["description"],
                            'thumbnails_high' : item["snippet"]["thumbnails"]["high"]["url"],
                            'thumbnails_medium' : item["snippet"]["thumbnails"]["medium"]["url"],
                            'thumbnails_default' : item["snippet"]["thumbnails"]["default"]["url"],
                            'channel_title' : item["snippet"]["channelTitle"],
                            'playlist_id' : item["snippet"]["playlistId"],
                            'video_owner_channel_title' : item["snippet"]["videoOwnerChannelTitle"],
                            'video_owner_channel_id' : item["snippet"]["videoOwnerChannelId"],
                            'published_at' : item["snippet"]["publishedAt"]
                          }
                      )
        
        '''

        #
        # 以下取得したvideoの情報をもとにstatistics情報を収集する処理
        #
        
        all_videos = Video.objects.all()   
        
        #ここから本当にyoutubeAPIをたたくための処理
        '''
        videoIds =[]
        
        for video in all_videos:
            videoIds.append(video.video_id)

        stat_list = get_video_statistics_info_by_videoids(videoIds)

        with open("video_stat_data.json","w") as file:
            json.dump(stat_list,file)
        
        '''
        #ここまで本当にYOutubeAPIをたたくための処理

            
        
        with open("video_stat_data.json","r") as file:
            videostat_list = json.load(file)

        

        final_video_stat_list = []
        for video in videostat_list:
                for video_item in video["items"]:
                     final_video_stat_list.append(video_item)

        for video_data in final_video_stat_list:
            try :
                obj = Video.objects.get(video_id = video_data["id"])
                obj.view_count = int(video_data["statistics"]["viewCount"])
                obj.favorite_count = int(video_data["statistics"]["favoriteCount"])
                if "commentCount" in video_data["statistics"]:
                    obj.comment_count = int(video_data["statistics"]["commentCount"])
                obj.save()
            except Exception as e:
                print("エラーが発生しました : " + video_data["id"])
                print(video_data["statistics"].keys())
                print(e)
        


           
        self.stdout.write(self.style.SUCCESS('Successfully executed command'))