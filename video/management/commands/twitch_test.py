from django.core.management.base import BaseCommand
from video.util.youtube_video_getter import get_latest_video_id_by_channel_ids,get_broadcasting_status_by_video_ids
from video.models import Channel
import requests
import json

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

# 配信情報を表示
        for stream in streams_data['data']:
            print(stream.keys())
            print(f'配信者: {stream["user_name"]},ユーザーID : {stream["id"]}, タイトル: {stream["title"]}, 視聴者数: {stream["viewer_count"]}')



        


    
        self.stdout.write('Batch process has been executed')

   