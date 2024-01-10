from django.shortcuts import render
from top.util.page_initializer import context_initializer
from .form import StreamSearchForm,StreamSortForm
from django.http import JsonResponse,HttpResponse
import redis

# Create your views here.


def index(request):
    """
    TEKKEN MANIAXのStream機能表示用View
    :param request:
    :return:
    """


    context = {}
    context = context_initializer(request, context)
    context['search_form'] = StreamSearchForm(request.GET)
    context['search_order_form'] = StreamSortForm(request.GET)
    return render(request, "stream/index.html", context)

def list_stream_endpoint(request):
    
    print("List_stream_endpoint:アクセスされてます")

    red = redis.Redis(host='localhost',port=6379,db=1)
    
    stream_count = int(red.get('stream_count'))
    
    print("stream_count : ")
    print(int(stream_count))

    streams = []

    for i in range(stream_count):
        print("i : " + str(i))
        print("streamer_value : " + str(red.hget(f"live_stream:{i}","streamer").decode('utf-8')))
        print("platform : " + str(red.hget(f"live_stream:{i}","platform").decode('utf-8')))
        print("url : " + str(red.hget(f"live_stream:{i}","url").decode('utf-8')))
        print("title : " + str(red.hget(f"live_stream:{i}","title").decode('utf-8')))
        print("started_at : " + str(red.hget(f"live_stream:{i}","started_at").decode('utf-8')))
        print("language : " + str(red.hget(f"live_stream:{i}","language").decode('utf-8')))
        print("thumbnail_url : " + str(red.hget(f"live_stream:{i}","thumbnail_url").decode('utf-8')))
        print("viewer_count : " + str(red.hget(f"live_stream:{i}","viewer_count").decode('utf-8')))

        streams.append(
            {
            "streamer_value" : str(red.hget(f"live_stream:{i}","streamer").decode('utf-8')),
            "platform" : str(red.hget(f"live_stream:{i}","platform").decode('utf-8')),
            "url" : str(red.hget(f"live_stream:{i}","url").decode('utf-8')),
            "title" :   str(red.hget(f"live_stream:{i}","title").decode('utf-8')),
            "started_at" :  str(red.hget(f"live_stream:{i}","started_at").decode('utf-8')),
            "language" :  str(red.hget(f"live_stream:{i}","language").decode('utf-8')),
            "thumbnail_url" : str(red.hget(f"live_stream:{i}","thumbnail_url").decode('utf-8')),
            "viewer_count" : str(red.hget(f"live_stream:{i}","viewer_count").decode('utf-8'))
        }
        )

    return JsonResponse({"streams" : streams},content_type='aplipcation/json')
