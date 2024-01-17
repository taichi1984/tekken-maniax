from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse,reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView,CreateView,UpdateView,DeleteView

from guide.util.make_guide_list import make_guide_list_with_evaluation
from top.forms import ChangeEmailForm
from .util import profile_manager
from .forms import UserProfileUpdateForm, UserCreationForm,CreateChangeLogForm,UpdateChangeLogForm
from .models import UserProfile, CustomUser, Notification,ChangeLog

from guide.models import Character, Guide
from django.db.utils import IntegrityError

# Create your views here.
from .util.page_initializer import context_initializer


#############################
# index画面
#############################

def index(request):
    """
    TEKKEN MANIAXのトップページ表示用View
    :param request:
    :return:
    """
    context = {}
    context = context_initializer(request, context)
    changeLog = ChangeLog.objects.all().order_by('pub_date')
    context["changeLog"] = changeLog
    return render(request, "top/index.html", context)

#############################
# 更新履歴の追加画面
#############################

class CreateChangeLog(CreateView):
    model = ChangeLog
    form_class = CreateChangeLogForm
    template_name = 'top/create_change_log.html'
    success_url = reverse_lazy('top:index')
    
class ListChangeLog(ListView):
    model = ChangeLog
    template_name= 'top/list_change_log.html'
    context_object_name = 'ChangeLog'
    pagenate_by = 20

class UpdateChangeLog(UpdateView):
    model = ChangeLog
    form_class = UpdateChangeLogForm
    template_name = 'top/update_change_log.html'
    success_url = reverse_lazy('top:index')

class DeleteChangeLog(DeleteView):
    model = ChangeLog
    success_url = reverse_lazy('top:list_change_log')
    template_name = 'top/delete_change_log.html'
    




#############################
# サイトに関しての説明関連画面 #
#############################

def how_to_register(request):
    context = {}
    context = context_initializer(request, context)
    return render(request, "top/how_to_register.html", context)


def notation(request):
    context = {}
    context = context_initializer(request, context)
    return render(request, 'top/notation.html', context)


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
        context = {}
        context = context_initializer(request, context)
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        password_check = request.POST.get('password_check')

        if form.is_valid():
            user = CustomUser.objects.create_user(username, email=email, password=password)
            UserProfile(user=user).save()
            login(request, user)
            return redirect("top:initialize_profile")
        else :
            form = UserCreationForm(request.POST)
            context['form']  = form
            return render(request, "top/register.html", context)

    else:  # はじめてきたとき
        form = UserCreationForm()
        context = {}
        context = context_initializer(request, context)
        context['form'] = form

        return render(request, "top/register.html", context)





# アカウント登録時の初回のみのプロフィール設定画面

def initialize_profile(request):
    user = request.user

    if user.is_authenticated:
        if request.method == "POST":
            profile_manager.save_profile(user=user, request=request)

            return redirect(reverse("top:registration_finish"))

        else:
            form = UserProfileUpdateForm()
            context = {}
            context = context_initializer(request, context)
            context['form'] = form
            return render(request, "top/initialize_profile.html", context)

    else:
        return redirect(reverse("top:index"))


# アカウントの登録完了画面
def registration_finish(request):
    context = {}
    context = context_initializer(request, context)
    return render(request, "top/registration_finish.html", context)


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
        context = context_initializer(request, context)
        return render(request, "top/account_manager.html", context)
    else:
        return redirect(reverse("login") + "?next=" + (reverse("top:account_manager")))


def delete_account(request):
    """
    アカウント削除画面
    :param request:
    :return:
    """
    if request.user.is_authenticated:
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

            context = {}
            context = context_initializer(request, context)
            return render(request, "top/delete_account_complete.html", context)
        else:
            context = {}
            context = context_initializer(request, context)
            return render(request, "top/delete_account.html", context)
    else:
        None

    return redirect(reverse("login") + "?next=" + (reverse("top:account_manager")))


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

            context = {'form': form}
            context = context_initializer(request, context)
            return render(request, "top/edit_profile.html", context)

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
    context = context_initializer(request, context)
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
    context = {}
    context = context_initializer(request, context)
    return render(request, "top/logout_complete.html", context)


# ユーザー情報閲覧ページ
def user_information(request, user_id):
    user_information = get_object_or_404(CustomUser, pk=user_id)
    user_guides = Guide.objects.filter(author=user_information, is_deleted=False, publishing_setting=1).order_by(
        'update_date').reverse()
    user_guides = make_guide_list_with_evaluation(user_guides)

    if not user_information.is_active:
        return redirect(reverse("guide:error") + "?error_message=ユーザーIDが正しくありません。")

    context = {
        'user_information': user_information,
        'guide_list': user_guides
    }
    context = context_initializer(request, context)
    return render(request, 'top/user_information.html', context)


# 通知ページ

class NotificationPage(LoginRequiredMixin, ListView):
    """
    検索画面用のView
    """
    model = Notification
    paginate_by = 20
    template_name = 'top/notification.html'
    context_object_name = 'notification_list'

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = context_initializer(self.request,context)
        return context;



def notification_check(request):
    """
    ガイド評価のajax用のview
    :param request:
    :return:
    """
    if request.method == "POST":
        notification_id = request.POST.get('notification_id')
        notification = Notification.objects.filter(id=notification_id).first()

        if notification.alreadyRead:
            notification.alreadyRead = False
        else:
            notification.alreadyRead = True
        notification.save()

    return HttpResponse("aaa")


def notification_check_all(request):
    if request.method == "POST":
        notification_id = request.POST.get('notification_id')
        notification_list = Notification.objects.filter(user=request.user)

        for notification in notification_list:
            print(notification.alreadyRead)
            notification.alreadyRead = True
            notification.save()

    return HttpResponse("aaa")


# エラーページ
def error(request):
    error_message = request.GET.get('error_message')
    context = {
        'error_message': error_message
    }
    context = context_initializer(request, context)
    return render(request, "top/error.html", context)

# Google AdSense ads.txt用


def ads(request):
    return render(request, 'top/ads.txt')


