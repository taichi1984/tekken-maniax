#database/urls.py

from django.urls import path

from . import views

app_name = "database"

urlpatterns = [
    # index page
    path('', views.index, name='index'),
    path('frame_data/',views.FrameDataIndexView.as_view(),name='frame_data_index'),
    path('frame_data/move_list/', views.MoveList.as_view(),name='move_list'),
    path('frame_data/move_detail/<int:pk>',views.MoveDetail.as_view(), name="move_detail"),
    path('frame_data/move_create/',views.MoveCreate.as_view(), name="move_create"),
    path('frame_data/move_create/success',views.moveCreateSuccess,name="move_create_success"),
    path('frame_data/move_update/<int:pk>',views.MoveUpdate.as_view(),name="move_update"),
]
