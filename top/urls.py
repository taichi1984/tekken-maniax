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
    path('account_manager/error/', views.error_account_manager, name='error_account_manager'),
    path('account_manager/delete_account/', views.delete_account, name='delete_account'),
    path('account_manager/change_email/', views.change_email, name='change_email'),
    path('account_manager/', views.account_manager, name='account_manager'),
    path('account_manager/profile/', views.edit_profile, name='profile'),
]
