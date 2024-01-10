##
##video/urls.py
##

from django.urls import path

from . import views

app_name = "video"

urlpatterns = [
    # index page
    path('', views.index, name='index'),
    path('channels/',views.ChannelsList.as_view(),name='channels'),
    path('channels/<int:pk>/',views.ChannelDetail.as_view(),name='channel_detail'),
    path('channels/<int:pk>/add_tag_endpoint/' , views.add_tag_endpoint, name='add_tag_endpoint'),
    path('channels/favorite/',views.ChannelFavorite.as_view(),name="channel_favorite"),
    path('youtube_stream_endpoint/',views.youtube_stream_endpoint, name='youtube_stream_endpoint'),
    path('add_favorite_ch/', views.add_favorite_ch ,name='add_favorite_ch')
]
