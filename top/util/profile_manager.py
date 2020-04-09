from top.models import UserProfile
from guide.models import Character


def save_profile(user, request):
    main_character = Character.objects.get(id=request.POST.get('main_character'))

    UserProfile(id=user.userprofile.id,
                nick_name=request.POST.get('nick_name'),
                main_character=main_character,
                twitter_account=request.POST.get('twitter_account'),
                youtube_channel_url=request.POST.get('youtube_channel_url'),
                twitch_url=request.POST.get('twitch_url'),
                introduction=request.POST.get('introduction'),
                user_id=user.id).save()
