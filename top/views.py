from django.contrib.auth import login, logout
from django.urls import reverse
from django.shortcuts import render, redirect

from top.forms import ChangeEmailForm
from .util import profile_manager
from .forms import UserProfileUpdateForm, UserCreationForm
from .models import UserProfile, CustomUser
from guide.models import Character, Guide
from django.db.utils import IntegrityError


# Create your views here.

def index(request):
    """
    TEKKEN MANIAXのトップページ表示用View
    :param request:
    :return:
    """
    return render(request, "top/index.html")


#############################
# サイトに関しての説明関連画面 #
#############################

def how_to_register(request):
    return render(request, "top/how_to_register.html")


def notation(request):
    return render(request, 'top/notation.html')


########################
# アカウント登録関連画面 #
########################

#
# アカウント登録画面
#

def register(request):
    """
    ユーザー登録用ページ
    :param request:
    :return:
    """
    # TODO このメソッドにはemailのバリデーションを行った際のエラー表示ができていないという問題点があります。
    # 　emailアドレスが他のユーザーと重複していた場合、validationではじくが、メールアドレスが間違っている旨が表示されない。
    # validationの設定方法が不明で現在放置中です。

    if request.method == 'POST':  # 投稿時処理
        form = UserCreationForm(request.POST)
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        password_check = request.POST.get('password_check')

        if form.is_valid():
            user = CustomUser.objects.create_user(username, email=email, password=password)
            UserProfile(user=user).save()
            login(request, user)
            return redirect("top:initialize_profile")

        form = UserCreationForm(request.POST)

    else:  # はじめてきたとき
        form = UserCreationForm()

    return render(request, "top/register.html", {'form': form})


# アカウント登録時の初回のみのプロフィール設定画面

def initialize_profile(request):
    user = request.user

    if user.is_authenticated:
        if request.method == "POST":
            profile_manager.save_profile(user=user, request=request)

            return redirect(reverse("top:registration_finish"))

        else:
            form = UserProfileUpdateForm()
            return render(request, "top/initialize_profile.html", {'form': form})
    else:
        return redirect(reverse("top:index"))


# アカウントの登録完了画面
def registration_finish(request):
    return render(request, "top/registration_finish.html")


##############################
# アカウントマネージャー関連画面 #
##############################

# アカウントマネージャートップ
def account_manager(request):
    """
    アカウントマネージャートップ画面
    """

    if request.user.is_authenticated:
        user = request.user
        guide_list = Guide.objects.filter(author=user)
        user = CustomUser.objects.get_by_natural_key(user)

        context = {
            'guide_list': guide_list,
            'current_user': user,
        }

        return render(request, "top/account_manager.html", context)
    else:
        return redirect(reverse("login") + "?next=" + (reverse("top:account_manager")))


def delete_account(request):
    """
    アカウント削除画面
    :param request:
    :return:
    """
    if request.method == 'POST':
        user = request.user
        guide_list = Guide.objects.filter(author=request.user)
        for guide in guide_list:
            print(guide)
            guide.is_deleted = True
            guide.save()

        user.is_active = False
        user.save()
        logout(request)
        return render(request, "top/delete_account_complete.html")
    else:
        None
    return render(request, "top/delete_account.html")


#
# profile編集画面
#

def edit_profile(request):
    """
    プロフィール編集画面
    :param request:
    :return:
    """
    user = request.user;

    if user.is_authenticated:
        if request.method == "POST":
            profile_manager.save_profile(user=user, request=request)

            return redirect(reverse("top:account_manager"))

        else:
            # UserProfileObjectがなかった場合は、空のUserProfileObjectを新規作成
            try:
                print(user.userprofile)
            except:
                UserProfile(user_id=user.id).save()

            initail_dict = {
                'nick_name': user.userprofile.nick_name,
                'main_character': user.userprofile.main_character,
                'twitter_account': user.userprofile.twitter_account,
                'youtube_channel_url': user.userprofile.youtube_channel_url,
                'twitch_url': user.userprofile.twitch_url,
                'introduction': user.userprofile.introduction,

            }

            form = UserProfileUpdateForm(initial=initail_dict)
            return render(request, "top/profile.html", {'form': form})

    else:
        return redirect(reverse("login") + "?next=" + (reverse("top:account_manager")))


def change_email(request):
    """
    e-mail変更画面
    :param request:
    :return:
    """
    user = request.user
    form = ChangeEmailForm()
    context = {
        'form': form
    }
    if user.is_authenticated:
        if request.method == "POST":
            try:
                user.email = request.POST.get("new_email")
                user.save()
            except:
                context = {
                    "error_message": "入力されたe-mailアドレスは既にほかのユーザーが登録しています。",
                }
                return render(request, "top/change_email.html", context)

            return render(request, "top/change_email_done.html")

    else:
        return redirect(reverse("login") + "?next=" + (reverse("top:account_manager")))

    return render(request, "top/change_email.html", context)


# ログアウト完了後のページ
def logout_complete(request):
    return render(request, "top/logout_complete.html")


# エラーページ
def error(request):
    error_message = request.GET.get('error_message')
    context = {
        'error_message': error_message
    }
    return render(request, "top/error.html", context)
