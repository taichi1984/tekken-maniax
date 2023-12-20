from django.core.management.base import BaseCommand
from video.util.youtube_video_getter import get_latest_video_id_by_channel_ids,get_broadcasting_status_by_video_ids
from video.models import Channel
import requests
import json
import redis

CLIENT_ID = "qmqxxv4nxlswgw41w6o5bjrk0oohcz"
OAUTH_TOKEN ="r4hoz0wqowtdri21ihktyvzmh32aff"

class Command(BaseCommand):
    help = 'Describe what the command does here'

    def handle(self, *args, **options):
        auth_params ={
            'client_id' : CLIENT_ID,
            'client_secret' : OAUTH_TOKEN,
            'grant_type' : 'client_credentials'
        }

        auth_url = 'https://id.twitch.tv/oauth2/token'
        auth_response = requests.post(auth_url,params=auth_params)
        auth_data = auth_response.json()
        access_token = auth_data['access_token']

        # 検索したいゲーム名
        game_name = 'Tekken 8'

# ゲーム名からゲームIDを取得
        game_url = f'https://api.twitch.tv/helix/games?name={game_name}'
        headers = {
            'Client-ID': CLIENT_ID,
            'Authorization': f'Bearer {access_token}'
        }
        game_response = requests.get(game_url, headers=headers)
        game_data = game_response.json()
        print(game_data)
        game_id = game_data['data'][0]['id']

        # ゲームIDを使用して配信情報を取得
        streams_url = f'https://api.twitch.tv/helix/streams?game_id={game_id}'
        streams_response = requests.get(streams_url, headers=headers)
        streams_data = streams_response.json()
        print(streams_data)
        red = redis.Redis(host='localhost',port=6379,db=1)
        live_channels=[]

        

# 配信情報を表示
        for stream in streams_data['data']:
            live_channels.append(
                {
                    'streamer':stream['user_name'] ,
                    'title':stream['title'],
                    'viewer_count':stream['viewer_count']
                }
            )            
        i = 0
        for channel in live_channels:
            key = f'live_stream:{i}'
            red.hset(key,'streamer',channel["streamer"])
            red.hset(key,'title',channel["title"])
            red.hset(key,'viewer_count',channel['viewer_count'])
            i = i + 1

        streamer_value = red.hget("live_stream:test2","streamer")
        print("streamer_value : " + str(streamer_value.decode('utf-8')))
        



    

    
        self.stdout.write('Batch process has been executed')

   