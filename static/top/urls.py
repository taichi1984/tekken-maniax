from django.urls import path, include

from . import views

app_name = "top"

urlpatterns = [
    # index page
    path('', views.index, name='index'),
    path('go_to_top_page/', views.go_to_top_page, name='top_page'),
    path('register/registration_finish', views.registration_finish, name="registration_finish"),
    path('register/initialize_profile', views.initialize_profile, name="initialize_profile"),
    path('register/', views.register, name='register'),
    path('account_manager/delete_account/', views.delete_account, name='delete_account'),
    path('account_manager/change_email/', views.change_email, name='change_email'),
    path('account_manager/', views.account_manager, name='account_manager'),
    path('account_manager/profile/', views.profile, name='profile'),
    #path('account_manager/profile/update_profile', views.update_profile, name='update_profile')
    ]




