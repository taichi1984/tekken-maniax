from django.urls import path, include

from . import views

app_name = "top"

urlpatterns = [
    # index page
    path('', views.index, name='index'),
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
]
