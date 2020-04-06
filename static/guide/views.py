"""
    TEKKEN GUIDEのview
"""

__author__ = "西森"
__status__ = ""
__version__ = "0.0.1"
__date__ = "2020/03/27"

from json import JSONDecodeError
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound
from django.template import loader
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from guide.forms import CommentSubmitForm, SearchGuideForm
from top.models import CustomUser
from .util import text_html_converter
from .models import Guide, Character, Category, GuideComment, Favorite, Evaluation
from _datetime import datetime
from django.views.generic import ListView

from urllib.parse import urlencode
import json
import markdown


def index(request):
    """
    トップ画面のview
    :param request:
    :return:HttpResponse
    """

    latest_guide_list = Guide.objects.filter(is_deleted=False, publishing_setting=1).order_by('pub_date').reverse()[:9]
    character_list = Character.objects.all()
    template = loader.get_template('guide/index.html')
    character_guide_list = {}

    for character in character_list:
        character_guide_info = {
                        "character":character,
                        "num" : Guide.objects.filter(character=character).count()
        }
        character_guide_list[character.first_name_en] = character_guide_info



    context = {
        'latest_guide_list': latest_guide_list,
        'character_guide_list': character_guide_list,


    }
    return HttpResponse(template.render(context, request))


############################
# 　ガイド作成画面の表示処理  #
############################

def create_guide(request):
    """
    ガイド作成画面の表示用view
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        character_list = Character.objects.order_by('id')
        category_list = Category.objects.order_by('id')
        template = loader.get_template('guide/create_guide.html')
        context = {
            'character_list': character_list,
            'category_list': category_list,
        }
        return HttpResponse(template.render(context, request))

    else:
        return redirect(reverse('top:login') + "?next=" + reverse('guide:create'))


def post_guide(request):
    """
    投稿処理のview
    :param request:
    :return:
    """
    character_list = Character.objects.order_by('id')
    guide_id = request.POST.get("guide_id")
    guide_character_id = request.POST.get("guide_character")
    guide_category_id = request.POST.get("guide_category")
    guide_title = request.POST.get("guide_title")
    guide_section_title = request.POST.getlist("guide_section_title")
    guide_section_article = request.POST.getlist("guide_section_article")
    guide_content = []
    user = CustomUser.objects.get(username=request.user)

    for title, article in zip(guide_section_title, guide_section_article):
        guide_content.append({"title": title, "article": article})

    guide_article = json.dumps(guide_content, ensure_ascii=False)
    print(guide_content)

    Guide(id=guide_id, author=user, title=guide_title,
          category_id=guide_category_id,
          character_id=guide_character_id,
          article=guide_article, pub_date=datetime.now(),
          update_date=datetime.now()).save()

    template = loader.get_template('guide/post.html')

    context = {}

    return HttpResponse(template.render(context, request))


def preview_guide(request):
    """

    :param request:
    :return:
    """
    character_list = Character.objects.order_by('id')
    guide_character_id = request.POST.get("guide_character")
    guide_character = [character for character in character_list if character.id == guide_character_id]
    category_list = Category.objects.order_by('id')
    guide_category_id = request.POST.get("guide_category")
    guide_category = [category for category in category_list if category.id == guide_category_id]
    guide_title = request.POST.get("guide_title")

    guide_section_title = request.POST.getlist("guide_section_title")
    guide_section_article = request.POST.getlist("guide_section_article")
    guide_sections = []

    for title, article in zip(guide_section_title, guide_section_article):
        converted_article = text_html_converter.convert_to_html(article)
        guide_sections.append({"title": title, "article": converted_article})

    template = loader.get_template('guide/preview.html')
    context = {
        'guide_title': guide_title,
        'guide_category': guide_category,
        'guide_character': guide_character,
        'guide_sections': guide_sections,
        'character_list': character_list,
        'category_list': category_list,
    }
    return HttpResponse(template.render(context, request))


##########################
# 　ガイドの閲覧画面の処理  #
##########################

def detail_guide(request, guide_id):
    """
    ガイド閲覧画面の表示処理
    :param request:
    :param guide_id:
    :return:
    """
    guide = get_object_or_404(Guide, pk=guide_id)
    if guide.is_deleted:
        return redirect(reverse("guide:error") + "?error=この記事は削除済みです")
    if guide.publishing_setting == 0 and (guide.author != request.user):
        return redirect(reverse("guide:error") + "?error=この記事は非公開です")

    # ページビュー数の追加
    guide.number_of_preview += 1;
    guide.save()

    #
    numof_good_evaluations = Evaluation.objects.filter(evaluation=1, guide=guide).count()
    numof_bad_evaluations = Evaluation.objects.filter(evaluation=2, guide=guide).count()
    evaluation = ""
    if request.user.is_authenticated:
        evaluation = Evaluation.objects.filter(evaluator=request.user, guide=guide).first()

    favorite = ""
    if request.user.is_authenticated:
        favorite = Favorite.objects.filter(user=request.user, guide=guide).first()

    character_list = Character.objects.order_by('id')
    category_list = Category.objects.order_by('id')
    comment_list = GuideComment.objects.filter(guide=guide, is_deleted=False)
    guide_sections = json.loads(guide.article)
    for this_guide in guide_sections:
        this_guide["article"] = text_html_converter.convert_to_html(this_guide["article"])

    form = CommentSubmitForm()
    context = {
        'guide': guide,
        'guide_sections': guide_sections,
        'character_list': character_list,
        'category_list': category_list,
        "form": form,
        "comment_list": comment_list,
        "numof_good_evaluations": numof_good_evaluations,
        "numof_bad_evaluations": numof_bad_evaluations,
        "evaluation": evaluation,
        "favorite": favorite,
    }

    return render(request, 'guide/detail.html', context)


# detail guide ページの評価部分のajax用のview
def vote_evaluation(request):
    """
    ガイド評価のajax用のview
    :param request:
    :return:
    """
    guide_id = request.POST.get('url').replace("http://localhost:8000/guide/detail/", "")
    guide = Guide.objects.filter(id=guide_id).first()

    evaluation_query = Evaluation.objects.filter(evaluator=request.user, guide=guide).first()

    # 評価が１回もされてなかった場合は空の評価を作成する。
    # TODO 関数化すべき　ここから

    if evaluation_query is None:
        evaluation_query = Evaluation(evaluator=request.user, evaluation=0, guide=guide).save()

    # goodが押されたとき
    if request.POST.get('vote') == "1":
        evaluation_query.evaluation = 1
        evaluation_query.save()

        evaluation_html = '<button type="button" class="good_evaluation_pushed_button" name="good_evaluation" value="good_evaluation">\
        <img src="/static/guide/image/good_evaluation.jpg" width="20px"></button>'

    # badが押されたとき
    elif request.POST.get('vote') == "2":
        evaluation_query.evaluation = 2
        evaluation_query.save()

        evaluation_html = '<button type="button" class="good_evaluation_pushed_button" name="good_evaluation" value="good_evaluation">\
        <img src="/static/guide/image/bad_evaluation.jpg" width="20px"></button>'

    # goodがキャンセルされたとき
    elif request.POST.get('vote') == "3":
        evaluation_query.evaluation = 0
        evaluation_query.save()
        evaluation_html = '<button type="button" class="good_evaluation_button" name="good_evaluation" value="good_evaluation">\
        <img src="/static/guide/image/good_evaluation.jpg" width="20px"></button>'

    # badがキャンセルされた時
    elif request.POST.get('vote') == "4":
        evaluation_query.evaluation = 0
        evaluation_query.save()
        evaluation_html = '<button type="button" class="good_evaluation_button" name="good_evaluation" value="good_evaluation">\
        <img src="/static/guide/image/bad_evaluation.jpg" width="20px"></button>'

    numof_good_evaluations = Evaluation.objects.filter(evaluation=1, guide=guide).count()
    numof_bad_evaluations = Evaluation.objects.filter(evaluation=2, guide=guide).count()
    data = []
    data[0] = evaluation_html
    data[1] = numof_good_evaluations
    data[2] = numof_bad_evaluations
    data = json.dumps(data)
    # ここまで

    return HttpResponse(data)


# detailのお気に入り追加のajax処理用view
def add_favorite(request):
    guide_id = request.POST.get('url').replace("http://localhost:8000/guide/detail/", "")
    guide = Guide.objects.filter(id=guide_id).first()

    # お気に入りに追加ボタンが押されたとき
    if request.POST.get('favorite') == "1":
        Favorite(user=request.user, guide=guide).save()
        favorite_html = '<button type="button" class="favorite_pushed_button" name="release_favorite">お気に入り追加済み</button>'

    # 　お気に入り解除ボタンが押されたとき
    else:
        favorite_query = Favorite.objects.filter(user=request.user, guide=guide).first()
        if favorite_query is not None:
            favorite_query.delete()

        favorite_html = '<button type="button" class="favorite_button" name="add_favorite">お気に入りに追加</button>'

    return HttpResponse(favorite_html)


def post_comment(request, guide_id):
    """
    コメント投稿時の処理
    :param request:
    :param guide_id:
    :return:
    """

    guide = get_object_or_404(Guide, pk=guide_id)
    contributor = request.user
    comment = text_html_converter.convert_to_html(request.POST.get("comment"))

    GuideComment(contributor=contributor, comment=comment, guide=guide, pub_date=datetime.now()).save()
    return redirect("guide:detail", guide_id=guide_id)


def delete_comment(request, comment_id):
    """
    コメント削除ボタン押下時の処理
    :param request:
    :param comment_id:
    :return:
    """
    print(request.POST.get('next'))
    comment = GuideComment.objects.filter(id=comment_id).first()
    guide_id = comment.guide.id
    comment.is_deleted = True
    comment.save()
    return redirect(request.POST.get('next'), guide_id=guide_id)


#####################################
# 投稿したガイドのリスト一覧画面の処理  #
#####################################
class YourGuide(ListView):
    """
    投稿したガイド一覧の表示用View
    """
    model = Guide
    paginate_by = 15
    template_name = 'guide/your_guide.html'
    context_object_name = 'guide_list'

    def get_queryset(self):
        return Guide.objects.filter(author=self.request.user)


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

class FavoriteGuide(ListView):
    """
    お気に入り画面表示用のView
    """
    model = Favorite
    paginate_by = 10
    template_name = 'guide/favorite_guide.html'
    context_object_name = 'favorite_list'

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)


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

        if search_word is not "":
            character = Character.objects.filter(Q(first_name_jp=search_word) |
                                                 Q(first_name_en=search_word) |
                                                 Q(family_name_jp=search_word) |
                                                 Q(family_name_en=search_word))
            category = Category.objects.filter(name=search_word)

            return Guide.objects.filter(Q(publishing_setting=1) &
                                        Q(is_deleted=False) &
                                        (Q(character=character.first()) |
                                         Q(category=category.first()) |
                                         Q(title__contains=search_word) |
                                         Q(article__contains=search_word))
                                        )
        else:
            return None


##########################
# ガイド更新画面用のview達 #
##########################

def update_guide(request, guide_id):
    """
    ガイドの更新画面用のview
    :param request:
    :param guide_id:
    :return:
    """
    guide = get_object_or_404(Guide, pk=guide_id)
    if request.user != guide.author:
        return redirect("top:top_page")

    if request.user.is_authenticated:
        character_list = Character.objects.order_by('id')
        category_list = Category.objects.order_by('id')
        template = loader.get_template('guide/update.html')
        article_list = json.loads(guide.article)

        context = {
            'guide': guide,
            'article_list': article_list,
            'character_list': character_list,
            'category_list': category_list,
        }
        return HttpResponse(template.render(context, request))

    else:
        return redirect(reverse('top:login'))

    return render(request, update_html)


####################
# エラー画面用のview #
####################
def guide_error(request):
    """
    エラー画面表示用のview
    :param request:
    :return:
    """

    error_text = request.GET.get('error')
    context = {
        'error_text': error_text
    }
    return render(request, 'guide/guide_error.html', context)
