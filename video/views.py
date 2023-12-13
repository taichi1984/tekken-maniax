# Create your views here.
##
##video/views.py
##

from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from top.util.page_initializer import context_initializer
from googleapiclient.discovery import build
from .models import Channel ,Video,Tag
from .forms import ChannelSearchForm,VideoSearchForm,ChannelSortForm,TagForm
from django.views.generic import ListView,DetailView
from django.db.models import Q
from django.http import JsonResponse,HttpResponse
import json
import feedparser


def index(request):
    """
    TEKKEN MANIAXのVideoページのindex表示用view
    """
    channelsData = Channel.objects.all()
    context = {"channelsData" : channelsData}
    context = context_initializer(request, context)
    
    
    return render(request, "video/index.html", context)
# Create your views here.

class ChannelsList(ListView):
    """
    チャンネルリスト表示用のビュー
    """
    model = Channel
    paginate_by = 20
    template_name = 'video/channels.html'
    context_object_name = 'channels'

    def get_queryset(self):
        queryset = super().get_queryset()
        #search = self.request.GET.get('search','')


        sort = self.request.GET.get('channel_sort_field','')
        query = self.request.GET.get('query','')    

        if query:
            queryset = queryset.filter(
                Q(channel_title__icontains=query) | 
                Q(tags__name__icontains=query)
                )


        if sort=='channel_sort_field':
            queryset = queryset.order_by('')

        elif sort == 'viewcount_desc':
            queryset = queryset.order_by('-viewcount')
        
        elif sort == 'viewcount_asc':
            queryset = queryset.order_by('viewcount')

        elif sort == 'subscribercount_desc':#登録者数降順
            queryset = queryset.order_by('-subscribercount')
        
        elif sort == 'subscribercount_asc':#登録者数昇順
            queryset = queryset.order_by('subscribercount')

        elif sort == 'videocount_desc':
            queryset = queryset.order_by('-videocount')
        
        elif sort == 'videocount_asc':
            queryset = queryset.order_by('videocount')
        
        return queryset
    
    def get_context_data(self,**kwargs):
        
        context = super().get_context_data(**kwargs)
        context['current_sort'] = self.request.GET.get('sort','videocount')
        context['search_form'] = ChannelSearchForm(self.request.GET)
        context['search_order_form'] = ChannelSortForm(self.request.GET)
        
        return context
    



class ChannelDetail(DetailView):
    """
    チャンネル詳細ページのview
    """

    model = Channel
    template_name = 'video/channel_detail.html'
    context_object_name ="channel"   

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['video_list'] = Video.objects.filter(video_owner_channel_id = self.object.channel_id)
        tags_data = context['channel'].tags.all()
        context['tags'] = json.dumps(list(tags_data.values()),ensure_ascii = False)
        return context
      
@csrf_exempt
def youtube_stream_endpoint(request):
    if request.method=='POST':
        print("YoutubeからのフィードをPOSTで受け取りました")
        print(request.body.decode(('utf-8')))
        feedinfo = feedparser.parse(request.body.decode(('utf-8')))
        print(feedinfo)


        return HttpResponse('success',content_type='text/plain',status=200)

    if request.method=='GET':
        print("youtubeからのフィードをgetで受け取りました")
        challenge = request.GET['hub.challenge']
        return HttpResponse(challenge,content_type='text/plain',status=200)
        
# Create your views here.
@csrf_exempt

def add_tag_endpoint(request,pk):
    if request.method=='POST':
        data=json.loads(request.body.decode(('utf-8')))
        print(data)
        if data['method'] == 'add':
           
            print("ajaxでpostで受け取れています")
        
            print(data['tagText'])
            print(data['channelId'])
            obj,created = Tag.objects.filter(name=data['tagText']).get_or_create(defaults={'name':data['tagText']})
            channel = Channel.objects.filter(id=pk).get()
            channel.tags.add(obj)

            tags = json.dumps(list(channel.tags.all().values()),ensure_ascii=False)

        elif data['method'] == 'delete':
            channel = Channel.objects.filter(id=pk).get()
            print(channel.tags.all())

            i = 0
            for tag in channel.tags.all():
                print(data['deleteTags'][i])
                if data['deleteTags'][i] == True:
                   channel.tags.remove(tag)
                i = i+1

            tags = json.dumps(list(channel.tags.all().values()),ensure_ascii=False)
            print(tags)

                
        
        return JsonResponse({'status' : 'success' , 'data' : data , 'tags' : tags})

    return JsonResponse({'status': 'invalid method'}, status=400)
    

    