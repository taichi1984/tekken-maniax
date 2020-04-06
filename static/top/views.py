from django.contrib.auth import login, logout
from django.urls import reverse
from django.shortcuts import render, redirect

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


def account_manager(request):
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
        return redirect(reverse("top:index"))


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
            guide.is_deleted = True
        user.is_active = False
        user.save()
        logout(request)
        return render(request, "top/delete_account_complete.html")
    else:
        None
    return render(request, "top/delete_account.html")


def profile(request):
    """
    プロフィール表示変更画面
    :param request:
    :return:
    """
    user = request.user;

    if user.is_authenticated:
        # UserProfileObjectがなかった場合は、空のUserProfileObjectを新規作成
        try:
            print(user.userprofile)
        except:
            UserProfile(user_id=user.id).save()

        initail_dict = {
            'nick_name': user.userprofile.nick_name,
            'main_character': user.userprofile.main_character,
            'introduction': user.userprofile.introduction,
        }

        form = UserProfileUpdateForm(initial=initail_dict)
        return render(request, "top/profile.html", {'form': form})

    else:
        return redirect(reverse("top:index"))


# トップページに飛ぶ前のクッションページ
def go_to_top_page(request):

    return render(request, "top/go_to_top_page.html")


def change_email(request):
    """
    e-mail変更画面
    :param request:
    :return:
    """
    context = {}
    if request.method == "POST":
        try:
            user = request.user
            user.email = request.POST.get("e-mail")
            user.save()
        except:
            context = {
                "error_message": "入力されたe-mailアドレスは既にほかのユーザーが登録しています。",
            }
            return render(request, "top/change_email.html", context)

        return render(request, "top/change_email_done.html")
    else:
        None

    return render(request, "top/change_email.html")


def update_profile(request):
    """
    プロフィール更新画面
    :param request:
    :return:
    """
    next_page = request.POST.get('next')
    user = request.user
    print(request.POST.get('main_character'))
    main_character = Character.objects.get(id=request.POST.get('main_character'))

    UserProfile(id=user.userprofile.id,
                nick_name=request.POST.get('nick_name'),
                main_character=main_character,
                introduction=request.POST.get('introduction'),
                user_id=user.id).save()

    return redirect(reverse(next_page))


# アカウント登録時の初回のみのプロフィール設定画面

def initialize_profile(request):
    form = UserProfileUpdateForm()
    return render(request, "top/initialize_profile.html", {'form': form})


def registration_finish(request):
    return render(request, "top/registration_finish.html")
