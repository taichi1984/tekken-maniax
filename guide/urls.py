from django.urls import path

from . import views

app_name = "guide"

urlpatterns = [
    # index page
    path('', views.index, name='index'),
    # search_result
    path('search/', views.Search.as_view(), name='search'),
    # create guide
    path('create/', views.create_guide, name='create'),
    # preview guide
    path('create/preview/', views.preview_guide, name='preview'),
    # preview guide
    path('create/finish/', views.create_guide_finish, name='create_guide_finish'),
    # update_guide
    path('update/<int:guide_id>', views.update_guide, name='update'),
    # character_guide_list
    path('character_guide/', views.CharacterGuide.as_view(), name='character_guide'),
    # delete_guide
    path('delete/', views.delete_guide, name='delete'),
    # detail
    path('detail/<int:guide_id>', views.detail_guide, name='detail'),
    # your_guide
    path('your_guide/', views.YourGuide.as_view(), name='your_guide'),
    # favorite_guide
    path('favorite_guide/', views.FavoriteGuide.as_view(), name='favorite_guide'),
    # change_state
    path('change_state/<int:guide_id>', views.change_state_guide, name='change_state_guide'),
    # post_comment
    path('post_comment/<int:guide_id>', views.post_comment, name='post_comment'),
    # delete_comment
    path('delete_comment/<int:comment_id>', views.delete_comment, name='delete_comment'),
    # vote_evaluation
    path('vote_evaluation/', views.vote_evaluation, name="vote_evaluation"),
    # add_favorite
    path('add_favorite/', views.add_favorite, name="add_favorite"),
    # error
    path('error/', views.guide_error, name="error"),
    # introductionページ類
    path('about_guide/', views.about_guide, name="about_guide"),
    path('how_to_write_guides/', views.how_to_write_guides, name="how_to_write_guides"),
    path('guides_for_begineers/', views.guides_for_beginners, name="guides_for_beginners"),

]
