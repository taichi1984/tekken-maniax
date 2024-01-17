from django.urls import path, include

from . import views

app_name = "top"

urlpatterns = [
    # index page
    path('', views.index, name='index'),
    path('create_change_log/',views.CreateChangeLog.as_view(),name='create_change_log'),
    path('list_change_log/',views.ListChangeLog.as_view(),name='list_change_log'),
    path('update_change_log/<int:pk>',views.UpdateChangeLog.as_view(),name='update_change_log'),
    path('delete_change_log/<int:pk>' ,views.DeleteChangeLog.as_view(),name='delete_change_log'),
    path('how_to_register/', views.how_to_register, name="how_to_register"),
    path('notation/', views.notation, name="notation"),
    path('register/registration_finish', views.registration_finish, name="registration_finish"),
    path('register/initialize_profile', views.initialize_profile, name="initialize_profile"),
    path('register/', views.register, name='register'),
    path('account_manager/error/', views.error, name='error'),
    path('account_manager/delete_account/', views.delete_account, name='delete_account'),
    path('account_manager/change_email/', views.change_email, name='change_email'),
    path('account_manager/', views.account_manager, name='account_manager'),
    path('account_manager/profile/', views.edit_profile, name='profile'),
    path('logout_complete/', views.logout_complete, name="logout_complete"),
    path('user_information/<int:user_id>', views.user_information, name="user_information"),
    path('notification/', views.NotificationPage.as_view(), name="notification"),
    path('notification_check/', views.notification_check, name="notification_check"),
    path('notification_check_all/', views.notification_check_all, name="notification_check_all"),
    path('ads.txt/', views.ads, name='ads'),
]
