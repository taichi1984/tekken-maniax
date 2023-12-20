##
##stream/urls.py
##

from django.urls import path

from . import views

app_name = "stream"

urlpatterns = [
    # index page
    path('', views.index, name='index'),
    path('list_stream_endpoint/',views.list_stream_endpoint,name="list_stream_endpoint")
]
