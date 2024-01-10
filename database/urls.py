#database/urls.py

from django.urls import path

from . import views

app_name = "database"

urlpatterns = [
    # index page
    path('', views.index, name='index'),
    path('move_list', views.MoveList.as_view(),name='move_list'),
    path('move_detail/<int:pk>',views.MoveDetail.as_view(), name="move_detail"),
    path('move_create/',views.MoveCreate.as_view(), name="move_create"),
    path('move_create/success',views.moveCreateSuccess,name="move_create_success"),
    path('move_update/<int:pk>',views.MoveUpdate.as_view(),name="move_update")
   

]
