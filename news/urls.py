#database/urls.py

from django.urls import path

from . import views

app_name = "news"

urlpatterns = [
    # index page
    path('', views.index, name='index'),

]
