from googleapiclient.discovery import build
import json,feedparser
API_KEY = 'AIzaSyAzdUg5IZX5xoMtkj0UZLNt7--Qsq5_20s' #tekkenmaniax0401のapi-key
#API_KEY = 'AIzaSyBF_gw77-z9Criuzc47gS1GcsSS31UjAZ4' #キックミーN森のAPI-key

def divide_list(input_list, chunk_size):
    # input_listをchunk_sizeのサイズで分割し、新しいリストのリストを返す
    return [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]


def get_video_statistics_info_by_videoids(videoIds):
    # YouTube APIクライアントの構築
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    divided_list = divide_list(videoIds,50)


# ビデオ情報の取得
    responseList = []

    for video_id_list in divided_list:

        video_id_list_string = ','.join(video_id_list)

        request = youtube.videos().list(
        part = 'statistics',
        id = video_id_list_string
        )
    
        response = request.execute()
        responseList.append(response)

    return responseList


def get_video_info_by_channel(channelId):
    youtube = build('youtube','v3',developerKey=API_KEY)

    channel_response = youtube.channels().list(
    part="contentDetails",
    id=channelId
    ).execute()

    uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    print("playlistid = " + uploads_playlist_id)
    try:
        playlist_response = youtube.playlistItems().list(
        part="snippet,contentDetails,status",
        playlistId=uploads_playlist_id,
        maxResults=20
        ).execute()
    except Exception as e:
        print("アップロードされた動画は存在しません")
        playlist_response = []


    return playlist_response     
    


def search_channel_list(search_term,max_pages=10):
    youtube = build('youtube','v3',developerKey=API_KEY)

     # 検索クエリの実行
    search_response = youtube.search().list(
        q=search_term,  # ここに検索ワードを入力
        part=['snippet'],
        type='channel',
        maxResults=50  # 結果の数（最大50まで）
        ).execute()
    # 検索結果の表示

    channels = search_response.get('items',[])
    next_page_token = search_response.get('nextPageToken')


    while next_page_token:
        search_response = youtube.search().list(
            q=search_term,
            part=['snippet'],
            type='channel',
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        channels += search_response.get('items', [])
        next_page_token = search_response.get('nextPageToken')
  
    return channels



#
#チャンネル情報を50件取得する
#

def get_channel_info_from_channelids(channel_ids):
    youtube = build('youtube','v3',developerKey=API_KEY)
    
    youtube_request = youtube.channels().list(
    part='snippet,contentDetails,statistics',
    id=','.join(channel_ids)
    )
    youtube_response = youtube_request.execute()

    return youtube_response

def get_latest_video_id_by_channel_ids(channel_ids):
    youtube_feed_url = "https://www.youtube.com/feeds/videos.xml?channel_id="
    video_id_list = []
    
    for channel_id in channel_ids:
        print(youtube_feed_url+channel_id)
        data = feedparser.parse(youtube_feed_url+channel_id)

        video_id_list.append({
            'channel_id':channel_id,
            'feed_url':youtube_feed_url + channel_id,
            'video_id': data['entries'][0]['yt_videoid'] if len(data['entries']) != 0 else ""
        })
        
    return video_id_list
    
def get_broadcasting_status_by_video_ids(video_ids):
    youtube = build('youtube','v3',developerKey=API_KEY)
    divided_list = divide_list(video_ids, 50)
    responseList = []
  
    for video_id_list in divided_list:
        video_id_list_string = ','.join(video_id_list)

        print(video_id_list_string)
        request = youtube.videos().list(
        part = 'snippet',
        id = video_id_list_string
        )

        response = request.execute()
        responseList.append(response)


    broadcast_status_list = []
    
    for res_list in responseList:
        for res in res_list["items"]:
            print(res.keys())
            broadcast_status_list.append(
                {
                    "video_id" : res["id"],
                    "channel_id" : res["snippet"]["channelId"],
                    "liveBroadcastContent" : res["snippet"]["liveBroadcastContent"]
                }
            )
        
    return broadcast_status_list

    

            
            


