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

from .util.make_guide_list import make_guide_list_with_evaluation


def index(request):
    """
    トップ画面のview
    :param request:
    :return:HttpResponse
    """

    latest_guide_list = Guide.objects.filter(is_deleted=False, publishing_setting=1).order_by('pub_date').reverse()[:10]
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
    return render(request, 'guide/about_guide.html')


def how_to_write_guides(request):
    """
    ガイドの書き方についての表示用view
    """
    return render(request, 'guide/how_to_write_guides.html')


def guides_for_beginners(request):
    """
    初心者向けのガイド紹介ページ
    """
    return render(request, 'guide/guides_for_beginners.html')


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
        if request.method == 'POST':
            character_list = Character.objects.order_by('id')
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

            new_guide = Guide(author=user, title=guide_title,
                              category_id=guide_category_id,
                              character_id=guide_character_id,
                              article=guide_article, pub_date=datetime.now(),
                              update_date=datetime.now())
            new_guide.save()

            return redirect(reverse('guide:create_guide_finish') + "?next=" + str(new_guide.id))

        else:
            character_list = Character.objects.order_by('id')
            category_list = Category.objects.order_by('id')
            template = loader.get_template('guide/create_guide.html')
            context = {
                'character_list': character_list,
                'category_list': category_list,
            }
            return render(request, 'guide/create_guide.html', context)

    else:
        return redirect(reverse('top:login') + "?next=" + reverse('guide:create'))


def create_guide_finish(request):
    """
    投稿完了画面の表示用View
    :param request:
    :return:
    """
    next = request.GET.get('next')
    context = {'next': next}
    return render(request, 'guide/create_guide_finish.html', context)


def preview_guide(request):
    """
    ガイドのプレビュー表示用のview
    :param request:
    :return:
    """

    guide_character_id = request.POST.get("guide_character")
    guide_character = Character.objects.filter(id=guide_character_id).first()
    guide_category_id = request.POST.get("guide_category")
    guide_category = Category.objects.filter(id=guide_category_id).first()
    guide_title = request.POST.get("guide_title")

    guide_section_title = request.POST.getlist("guide_section_title")
    guide_section_article = request.POST.getlist("guide_section_article")
    guide_sections = []

    for title, article in zip(guide_section_title, guide_section_article):
        converted_article = text_html_converter.convert_to_html(article)
        print(converted_article)
        guide_sections.append({"title": title, "article": converted_article})

    template = loader.get_template('guide/preview.html')
    context = {
        'user': request.user,
        'guide_title': guide_title,
        'guide_category': guide_category,
        'guide_character_id': guide_character_id,
        'guide_character': guide_character,
        'guide_sections': guide_sections,

        'pub_date': datetime.now()
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
    comment_list = GuideComment.objects.filter(guide=guide)
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
    print(request.COOKIES)
    response = render(request, 'guide/detail.html', context)

    return response


# detail guide ページの評価部分のajax用のview
def vote_evaluation(request):
    """
    ガイド評価のajax用のview
    :param request:
    :return:
    """
    # 　TODO 本番環境と開発環境を問わないようにする場当たり的な対応のため、必ず直すこと。
    guide_id = request.POST.get('url').replace("http://localhost:8000/guide/detail/", "")
    guide_id = guide_id.replace("https://extreme-gamers.info/guide/detail/", "")

    guide = Guide.objects.filter(id=guide_id).first()

    evaluation_query = Evaluation.objects.filter(evaluator=request.user, guide=guide).first()

    # 評価が１回もされてなかった場合は空の評価を作成する。
    # TODO 関数化すべき　ここから

    if evaluation_query is None:
        evaluation_query = Evaluation(evaluator=request.user, evaluation=0, guide=guide)
        evaluation_query.save()

    # goodが押されたとき
    if request.POST.get('vote') == "1":
        evaluation_query.evaluation = 1
        evaluation_query.save()

        evaluation_html = '<button type="button" class="good_evaluation_pushed_button" name="good_evaluation_pushed" value="good_evaluation">\
        <img src="/static/guide/image/good_evaluation.jpg" width="20px"></button>'

    # badが押されたとき
    elif request.POST.get('vote') == "2":
        evaluation_query.evaluation = 2
        evaluation_query.save()

        evaluation_html = '<button type="button" class=" bad_evaluation_pushed_button" name="bad_evaluation_pushed" value="bad_evaluation">\
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
        evaluation_html = '<button type="button" class="bad_evaluation_button" name="bad_evaluation" value="bad_evaluation">\
        <img src="/static/guide/image/bad_evaluation.jpg" width="20px"></button>'

    numof_good_evaluations = Evaluation.objects.filter(evaluation=1, guide=guide).count()
    numof_bad_evaluations = Evaluation.objects.filter(evaluation=2, guide=guide).count()
    data = []
    data.append(evaluation_html)
    data.append(numof_good_evaluations)
    data.append(numof_bad_evaluations)
    data = json.dumps(data)
    # TODO 関数化すべき　ここまで

    return HttpResponse(data)


# detailのお気に入り追加のajax処理用view
def add_favorite(request):
    # TODO 場当たり的な対応で本番環境と開発環境の差異を吸収しているため訂正すること
    guide_id = request.POST.get('url').replace("http://localhost:8000/guide/detail/", "")
    guide_id = guide_id.replace("https://extreme-gamers.info/guide/detail/", "")
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
    comment = request.POST.get("comment")

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
        return Guide.objects.filter(author=self.request.user, is_deleted=False).order_by('-update_date')


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
        if request.method == 'POST':
            character_list = Character.objects.order_by('id')
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
            print("更新時id : " + str(guide.id))
            guide.author = user;
            guide.title = guide_title;
            guide.category_id = guide_category_id;
            guide.character_id = guide_character_id;
            guide.article = guide_article;
            guide.update_date = datetime.now();
            guide.save();

            return redirect(reverse('guide:create_guide_finish') + "?next=" + str(guide.id))
        else:
            character_list = Character.objects.order_by('id')
            category_list = Category.objects.order_by('id')
            template = loader.get_template('guide/update.html')
            article_list = json.loads(guide.article)

            print("表示時id : " + str(guide.id))
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
