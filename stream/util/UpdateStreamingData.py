from django.core.management.base import BaseCommand
from video.util.youtube_video_getter import get_latest_video_id_by_channel_ids,get_broadcasting_status_by_video_ids
from video.models import Channel,Video
import requests
import json
import redis
import asyncio

def UpdateYoutubeStreamingInfo(stream_count):
    """
    この関数はYoutubeの情報をredisサーバーに記録して、記録した件数を返す関数です。
    
    Args:

    Returns:Redisに登録した件数

    Raises:

    Examples:

    
    """

    channels = Channel.objects.all()
    channel_ids = []
    for channel in channels:
        channel_ids.append(channel.channel_id)

    video_id_list = asyncio.run(get_latest_video_id_by_channel_ids(channel_ids))
        
    '''
        #DBに最新の動画情報を保存する。redisでやるのでいったんコメントアウト
        for video_id in video_id_list:
            channel = Channel.objects.filter(channel_id = video_id["channel_id"]).get()
            channel.latest_video_id = video_id["video_id"]
            channel.save()
    '''

    video_ids = []
    for video_id in video_id_list:
        video_ids.append(video_id)

    broadcasting_status_list = get_broadcasting_status_by_video_ids(video_ids)
    
    count = stream_count
    print("Youtube前count : " + str(count))
    red = redis.Redis(host='localhost',port=6379,db=1)

    for broadcast_status in broadcasting_status_list:
        if broadcast_status["liveBroadcastContent"] == "live":
            print("youtube登録直前カウント : " +str(count))
            key = f'live_stream:{count}'
            ch = Channel.objects.filter(channel_id=broadcast_status["channel_id"]).get()
            red.hset(key,'streamer',ch.channel_title)
            red.hset(key,'platform',"Youtube")
            red.hset(key,'url',f"https://www.youtube.com/watch?v={broadcast_status['video_id']}")
            red.hset(key,'title',broadcast_status["video_title"])
            red.hset(key,'started_at',broadcast_status["actualStartTime"])
            red.hset(key,'language',"")
            red.hset(key,'thumbnail_url',broadcast_status["thumbnail_high"]["url"])
            if broadcast_status["concurrentViewers"] == "" :
                red.hset(key,'viewer_count',"0")
            else :
                red.hset(key,'viewer_count',broadcast_status["concurrentViewers"])
            count = count + 1

    return count

    


def UpdateTwitchStreamingInfo(stream_count):
    """
    この関数はtwitchの情報をredisサーバーに記録して、記録した件数を返す関数です。
    
    Args:

    Returns:redisに登録した件数

    Raises :

    Example:


    """
    
    CLIENT_ID = "qmqxxv4nxlswgw41w6o5bjrk0oohcz"
    OAUTH_TOKEN ="r4hoz0wqowtdri21ihktyvzmh32aff"

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
                'platform':"twitch",
                'title':stream['title'],
                'started_at':stream['started_at'],
                'language':stream['language'],
                'thumbnail_url':stream['thumbnail_url'].replace("{width}","500").replace("{height}","300"),
                'viewer_count':stream['viewer_count'],
            }
        )            
    count = stream_count
    for channel in live_channels:
        key = f'live_stream:{count}'
        red.hset(key,'streamer',channel["streamer"])
        red.hset(key,'platform',"twitch")
        red.hset(key,'url',"https://www.twitch.tv/" + channel["streamer"])
        red.hset(key,'title',channel["title"])
        red.hset(key,'started_at',channel["started_at"])
        red.hset(key,'language',channel["language"])
        red.hset(key,'thumbnail_url',channel["thumbnail_url"])
        red.hset(key,'viewer_count',channel['viewer_count'])
    
        count = count + 1

    return count