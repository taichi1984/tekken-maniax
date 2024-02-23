"""
    TEKKEN GUIDEのview
"""
__author__ = "西森"
__status__ = ""
__version__ = "0.0.1"
__date__ = "2020/03/27"

import os
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from json import JSONDecodeError
from .constants import GUIDE_INITIAL_DATA
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound,HttpResponseRedirect,HttpResponseForbidden
from django.template import loader
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from guide.forms import CommentSubmitForm, SearchGuideForm,CreateGuideForm,UpdateGuideForm
from top.models import CustomUser, Notification
from top.util.page_initializer import context_initializer
from .util import text_html_converter
from .models import Guide, Character, Category, GuideComment, Favorite, Evaluation
from datetime import datetime
from django.views.generic import ListView,CreateView,DetailView,UpdateView
from .serializers import CommentSerializer
import re
from urllib.parse import urlencode
import json
import markdown
from .util.generate_table_of_contents import generate_table_of_contents


from .util.make_guide_list import make_guide_list_with_evaluation


def index(request):
    """
    トップ画面のview
    :param request:
    :return:HttpResponse
    """

    latest_guide_list = Guide.objects.filter(is_deleted=False, publishing_setting=1).order_by('update_date').reverse()[
                        :10]
    guide_list = make_guide_list_with_evaluation(latest_guide_list)
    character_list = Character.objects.all()
    template = loader.get_template('guide/index.html')
    character_guide_list = {}
    for character in character_list:
        character_guide_info = {
            "character": character,
            "num": Guide.objects.filter(character=character, publishing_setting=1, is_deleted=False).count()
        }
        character_guide_list[character.first_name_en] = character_guide_info

    context = {
        'latest_guide_list': guide_list,
        'character_guide_list': character_guide_list,

    }
    context = context_initializer(request, context)
    return HttpResponse(template.render(context, request))


############################
# ガイドの説明関連画面の処理 #
############################

def about_guide(request):
    """
    ガイドについて画面の表示用view
    :param request:
    :return :
    """

    context = {}
    context = context_initializer(request, context)
    return render(request, 'guide/about_guide.html', context)


def how_to_write_guides(request):
    """
    ガイドの書き方についての表示用view
    """
    context = {}
    context = context_initializer(request, context)
    return render(request, 'guide/how_to_write_guides.html', context)


def guides_for_beginners(request):
    """
    初心者向けのガイド紹介ページ
    """
    context = {}
    context = context_initializer(request, context)
    return render(request, 'guide/guides_for_beginners.html', context)


############################
# 　ガイド作成画面の表示処理  #
############################

class CreateGuide(LoginRequiredMixin,CreateView):
    model = Guide
    form_class = CreateGuideForm
    template_name = "guide/create_guide.html"
    initial_data = GUIDE_INITIAL_DATA


    def get_initial(self):
        initial = super().get_initial()
        initial['article'] = self.initial_data

        return initial
    
    def form_valid(self,form):
        form.instance.author = self.request.user
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        if self.object:
            next = self.object.id
            success_url = reverse('guide:create_guide_finish')
            success_url += "?next=" + str(next)
            return success_url
        else:
            return super().get_success_url()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = context_initializer(self.request, context)
        return context
        
###########################
# プレビュー画面表示処理   #
##########################
    
def preview_guide(request):
    return HttpResponse("aaa")


##########################
# 　ガイドの閲覧画面の処理  #
##########################
class DetailGuide(DetailView):
    model = Guide
    template_name = 'guide/detail.html'
    context_object_name = "guide"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context = context_initializer(self.request,context)

        html_content = self.object.article
        table_of_contents,soup = generate_table_of_contents(html_content)
        
        self.object.article = soup.prettify()
        self.object.number_of_preview += 1
        self.object.save()
        context['table_of_contents'] = table_of_contents
        guide_id = self.object.id
        guide = Guide.objects.filter(id=guide_id).get()
        user = self.request.user
        try:
            context["favorite"] = Favorite.objects.filter(user=user,guide=guide).get()
        except :
            context["favorite"] = None

        try:
            context["evaluation"] = Evaluation.objects.filter(user=user,guide=guide).get()
        except :
            context["evaluation"] = None

        context["evaluationsCount"] = Evaluation.objects.filter(guide=guide).count()
      
        return context


@api_view(['POST'])
def vote_evaluation(request):
    """
    ガイド評価のajax用のview
    :param request:
    :return:
    """
    # TODO 本番環境と開発環境を問わないようにする場当たり的な対応のため、できれば直したい。
    guide_id = request.data.get("guide_id",None)
    guide = Guide.objects.filter(id=guide_id).first()

    evaluation_query = Evaluation.objects.filter(evaluator=request.user, guide=guide).first()

    # 評価が１回もされてなかった場合は空の評価を作成する。
    # TODO 関数化すべき　ここから

    # goodが押されたとき

    if request.data.get('vote') == 1:
        evaluation_query = Evaluation(evaluator=request.user, evaluation=0, guide=guide)
        evaluation_query.evaluation = 1
        evaluation_query.save()

    # goodがキャンセルされたとき
    else :
        evaluation_query.delete()
    
    data = {}
    evaluationsCount = Evaluation.objects.filter(evaluation=1, guide=guide).count()

    data["evaluationsCount"] = evaluationsCount
    # TODO 関数化すべき　ここまで
    print(data)
    return Response(data)


# detailのお気に入り追加のajax処理用view
@api_view(['POST'])
def add_favorite(request):

    guide_id = request.data.get("guide_id",None)
    guide = Guide.objects.filter(id=guide_id).first()

    # お気に入りに追加ボタンが押されたとき
    if request.data.get('favorite') == 1:
        favorite = Favorite(user=request.user, guide=guide).save()
  

    # 　お気に入り解除ボタンが押されたとき
    else:
        favorite_query = Favorite.objects.filter(user=request.user, guide=guide).first()
        

        if favorite_query is not None:
            favorite_query.delete()

        favorite_html = '<button type="button" class="favorite_button" name="add_favorite">お気に入りに追加</button>'

    return Response()


###############################
# detail画面でのコメント表示用API
###############################

@api_view(['GET'])
def list_comment(request):
    guide_id = request.GET["guide_id"]
    guide = Guide.objects.filter(id=guide_id).get()
    comments = GuideComment.objects.filter(guide=guide)
    serializer = CommentSerializer(comments,many=True)

    return Response(serializer.data)

################################
# detail画面でのコメント投稿用API
################################

@api_view(['POST'])
def post_comment(request, guide_id):
    """
    コメント投稿時の処理
    :param request:
    :param guide_id:
    :return:
    """
    if request.method == ('POST'):
        guide = get_object_or_404(Guide, pk=guide_id)
        contributor = request.user
        print(request.user.id)
        comment = request.data.get("comment",None)
        
        GuideComment(contributor=contributor, comment=comment, guide=guide, pub_date=timezone.now()).save()

        ###通知生成ここから
        if os.name == 'nt':  # 開発環境用コード
            notification_text = "あなたのガイド「<a href='http://localhost:8000/guide/detail/" + str(guide.id) + "'>" + str(
                guide.title) + "</a>」に" + contributor.userprofile.nick_name + "(id: " + contributor.username + ") さんがコメントを投稿しました"
        else:  # 本番環境用コード
            notification_text = "あなたのガイド「<a href='https://extreme-gamers.info/guide/detail/" + str(guide.id) + "'>" + str(
            guide.title) + "</a>」に" + contributor.userprofile.nick_name + "(id: " + contributor.username + ") さんがコメントを投稿しました"

        Notification(user=guide.author, notification_text=notification_text, alreadyRead=False,
                 pub_date=timezone.now()).save()

    ###通知生成ここまで

        guide = Guide.objects.filter(id=guide_id).get()
        comments = GuideComment.objects.filter(guide=guide)
        serializer = CommentSerializer(comments,many=True)
        data = serializer.data
        return Response(data=data,status=HTTP_201_CREATED)
   
###################################
# コメント削除用API
###################################

@api_view(['POST'])
def delete_comment(request):
    """
    コメント削除ボタン押下時の処理
    :param request:
    :param comment_id:
    :return:
    """
    if request.method == ('POST'):
        comment_id = request.data.get("d_comment_id",None)
        guide_id = request.data.get("guide_id",None)
        comment = GuideComment.objects.filter(id=comment_id).first()
        comment.is_deleted = True
        comment.save()
        guide = Guide.objects.filter(id=guide_id).get()
        comments = GuideComment.objects.filter(guide=guide)
        serializer = CommentSerializer(comments,many=True)
        data = serializer.data
    return Response(data=data,status=HTTP_201_CREATED)


##########################
# ガイド更新画面用のview達 #
#########################

class UpdateGuide(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Guide
    form_class = UpdateGuideForm
    template_name = "guide/update.html"
    
    def form_valid(self, form):
        # フォームのデータが有効な場合にのみ更新日時を設定
        self.object = form.save(commit=False)
        self.object.update_date = timezone.now()
        self.object.save()
        return super(UpdateGuide, self).form_valid(form)
        
    def test_func(self):
        # ユーザーが記事の著者かどうかをチェック
        return self.request.user == self.get_object().author

    def handle_no_permission(self):
        return HttpResponseForbidden("403 Forbidden: このページを編集する権限はありません。")
        
    def get_success_url(self):
        next = self.object.id
        success_url = reverse('guide:create_guide_finish')
        success_url += "?next=" + str(next)
        return success_url

###########################################
#  ガイド作成、ガイド更新処理後の遷移用ページ #
###########################################
def create_guide_finish(request):
    """
    投稿完了画面の表示用View
    :param request:
    :return:
    """
    next = request.GET.get('next')
    context = {'next': next}
    context = context_initializer(request, context)
    return render(request, 'guide/create_guide_finish.html', context)




#####################################
# 投稿したガイドのリスト一覧画面の処理  #
#####################################

class YourGuide(LoginRequiredMixin, ListView):
    """
    投稿したガイド一覧の表示用View
    """
    model = Guide
    paginate_by = 15
    template_name = 'guide/your_guide.html'
    context_object_name = 'guide_list'

    def get_queryset(self):
        return Guide.objects.filter(author=self.request.user, is_deleted=False).order_by('-update_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = context_initializer(self.request, context)
        return context


###
### guideの公開設定の変更用ビュー
###

def change_state_guide(request, guide_id):
    """
    :param request:
    :param guide_id:
    :return:
    """
    guide = Guide.objects.filter(id=guide_id).first()
    if guide.publishing_setting == 0:
        guide.publishing_setting = 1
    else:
        guide.publishing_setting = 0
    guide.save()
    return redirect("guide:your_guide")

#
# ガイドを削除する処理
#

def delete_guide(request):
    """
    ガイド削除ボタン押下時の処理
    :param request:
    :return:
    """

    if request.method == "POST":
        guide_id = request.POST.get("guide_id")
        print("ガイドＩＤは : " + guide_id)
        guide = Guide.objects.filter(id=guide_id).first()
        guide.is_deleted = True
        guide.save()
    else:
        return redirect(reverse("guide:index"))

    return redirect(reverse("guide:your_guide"))


########################
# お気に入りガイドの画面  #
########################

class FavoriteGuide(LoginRequiredMixin, ListView):
    """
    お気に入り画面表示用のView
    """
    model = Favorite
    paginate_by = 10
    template_name = 'guide/favorite_guide.html'
    context_object_name = 'favorite_list'

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = context_initializer(self.request, context)
        return context


###################################
#  キャラクター別ガイド一覧画面のView #
###################################
class CharacterGuide(ListView):
    """
    キャラクター一覧画面用のView
    """
    model = Guide
    paginate_by = 10
    template_name = 'guide/character_guide.html'
    context_object_name = 'guide_list'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['number_of_guide'] = len(self.object_list)
        character = Character.objects.filter(id=int(self.request.GET.get('character'))).first()
        context['character'] = character
        context = context_initializer(self.request, context)
        return context

    def get_queryset(self):
        return make_guide_list_with_evaluation(
            Guide.objects.filter(character=self.request.GET.get('character'), is_deleted=False,
                                 publishing_setting=1).order_by('-update_date'))


######################
# 　検索画面用のview   #
######################

class Search(ListView):
    """
    検索画面用のView
    """
    model = Guide
    paginate_by = 10
    template_name = 'guide/search.html'
    context_object_name = 'guide_list'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['form'] = SearchGuideForm()
        context['number_of_guide'] = len(self.object_list)
        context['search_word'] = self.request.GET.get('search_word')
        context = context_initializer(self.request, context)
        return context

    def get_queryset(self):
        search_word = self.request.GET.get('search_word')
        if search_word is not None:  # 検索除外ワードをはじく処置
            search_word = search_word.replace("{", "")
            search_word = search_word.replace("}", "")
            search_word = search_word.replace(":", "")
            search_word = search_word.replace(",", "")
        else:
            return None

        if search_word != "":
            character = Character.objects.filter(Q(first_name_jp=search_word) |
                                                 Q(first_name_en=search_word) |
                                                 Q(family_name_jp=search_word) |
                                                 Q(family_name_en=search_word))
            category = Category.objects.filter(name=search_word)

            return make_guide_list_with_evaluation(Guide.objects.filter(Q(publishing_setting=1) &
                                                                        Q(is_deleted=False) &
                                                                        (Q(character=character.first()) |
                                                                         Q(category=category.first()) |
                                                                         Q(title__contains=search_word) |
                                                                         Q(article__contains=search_word))
                                                                        ).order_by('-update_date'))
        else:
            return None




####################
# エラー画面用のview #
####################
def guide_error(request):
    """
    エラー画面表示用のview
    :param request:
    :return:
    """

    error_text = request.GET.get('error_message')
    context = {
        'error_text': error_text
    }
    context = context_initializer(request, context)
    return render(request, 'guide/guide_error.html', context)
