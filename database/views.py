##
##database/views.py
##

from django.shortcuts import render
from django.db.models import IntegerField,CharField, Value, Case, When, F
from top.util.page_initializer import context_initializer
from guide.models import Character
from django.views.generic import ListView,DetailView,CreateView,UpdateView
from .models import Move,MoveType
from .form import CreateMoveForm,UpdateMoveForm,MoveSortForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
import re
from django.urls import reverse
from operator import itemgetter
from .util.add_full_command import add_full_command_jp

def index(request):
    """
    TEKKEN MANIAXのデータベースページの表示用View
    :param request:
    :return:
    """
    context = {}
    context = context_initializer(request, context)
    context["character_list"] = Character.objects.all()
    
    return redirect(reverse("database:frame_data_index"))


class FrameDataIndexView(ListView):
    model = Character
    template_name = "database/frame_data.html"
    context_object_name = 'character_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = context_initializer(self.request, context)
        return context

##以下movelist

custom_order = {
        "ヒート発動可能":1,
        "LP+RK":51,
        "RP+LK":52,
        "LP":5,
        "RP":10,
        "LK":20,
        "RK":30,
        "WP":40,
        "WK":50,
        "【":60,
        "641236":220,
        "6n23":210,
        "666":180,
        "66_":170,
        "44_":175,
        "6n":160,
        "6LP+RK":77,
        "6RP+LK":78,
        "6LP":71,
        "6RP":72,
        "6LK":73,
        "6RK":74,
        "6WP":75,
        "6WK":76,
        "6":79,
        "3LP+RK":87,
        "3RP+LK":88,
        "3LP":81,
        "3RP":82,
        "3LK":83,
        "3RK":84,
        "3WP":85,
        "3WK":86,
        "3":89,
        "236":200,
        "2LP+RK":97,
        "2RP+LK":98,
        "2LP":91,
        "2RP":92,
        "2LK":93,
        "2RK":94,
        "2WP":95,
        "2WK":96,
        "2":99,
        "1LP+RK":107,
        "1RP+LK":108,
        "1LP":101,
        "1RP":102,
        "1LK":103,
        "1RK":104,
        "1WP":105,
        "1WK":106,
        "1":109,
        "44_":190,
        "4LP+RK":116,
        "4RP+LK":117,
        "4LP":110,
        "4RP":111,
        "4LK":112,
        "4RK":113,
        "4WP":114,
        "4WK":115,
        "4":118,
        "7LP+RK":127,
        "7RP+LK":128,
        "7LP":121,
        "7RP":122,
        "7LK":123,
        "7RK":124,
        "7WP":125,
        "7WK":126,
        "7":129,
        "8LP":131,
        "8RP":132,
        "8LK":133,
        "8RK":134,
        "8WP":135,
        "8WK":136,
        "8LP+RK":137,
        "8RP+LK":138,
        "8":139,
        "9LP+RK":147,
        "9RP+LK":148,
        "9LP":141,
        "9RP":142,
        "9LK":143,
        "9RK":144,
        "9WP":145,
        "9WK":146,
        "9":147,
        "9n":150,
        "46":155,
        "立ち途中に":230,
        "しゃがんだ状態で":240,
        "ヒート状態で":260,
        "レイジ状態で":270,
        "横移動中に":280,
        "相手に接近して":290,
        "相手の左側面から接近して":300,
        "相手の右側面から接近して":310,
        "相手の背後から接近して":320,
        "(相手ダウン中に)":330,
    }



def custom_order_key(obj):
    '''
    match = re.match(r'(\d+|[^0-9]+)', obj.full_command_jp)
    if match:
        key_part = match.group()
        print("match : " + key_part)
        return custom_order.get(key_part, len(custom_order)), key_part
    else:
        print("unmatch : " + key_part)
        return (len(custom_order),obj.full_command_jp)
    '''
  
    for key, value in custom_order.items():
        if obj.full_command_jp.startswith(key):
            return value
            #return (value,obj.full_command_jp)

    return len(custom_order)



class MoveList(ListView):
    """
    キャラごとのフレームデータの表示用View
    """
    model = Move
    template_name = 'database/move_list.html'
    context_object_name = 'move_list'


    def get_queryset(self):
        character_obj = Character.objects.filter(id = self.request.GET["character"]).get()
        queryset= Move.objects.filter(character=character_obj)

        queryset = add_full_command_jp(queryset)
        
        sort = self.request.GET.get('move_sort_field','command')

        if sort =='command':
            queryset = sorted(queryset,key=custom_order_key)

        elif sort == 'damage_desc':
            queryset = queryset.order_by("-damage")
            queryset = add_full_command_jp(queryset)
        
        elif sort == 'damage_asc':
            queryset = queryset.order_by('damage')
            queryset = add_full_command_jp(queryset)

        elif sort == 'frame_startup_desc':
            queryset = queryset.order_by('-frame_startup')
            queryset = add_full_command_jp(queryset)
        
        elif sort == 'frame_startup_asc':
            queryset = queryset.order_by('frame_startup')
            queryset = add_full_command_jp(queryset)

        elif sort == 'frame_block_desc':
            queryset = queryset.order_by('-frame_block')
            queryset = add_full_command_jp(queryset)
        
        elif sort == 'frame_block_asc':
            queryset = queryset.order_by('frame_block')
            queryset = add_full_command_jp(queryset)
        
        elif sort == 'frame_hit_desc':
            queryset = queryset.order_by('-frame_hit')
            queryset = add_full_command_jp(queryset)
        
        elif sort == 'frame_hit_asc':
            queryset = queryset.order_by('frame_hit')
            queryset = add_full_command_jp(queryset)

        elif sort == 'frame_counter_desc':
            queryset = queryset.order_by('-frame_counter')
            queryset = add_full_command_jp(queryset)
        
        elif sort == 'frame_counter_asc':
            queryset = queryset.order_by('frame_counter')
            queryset = add_full_command_jp(queryset)


        return queryset



        sort = self.request.GET.get('channel_sort_field','viewcount_desc')
        

        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = context_initializer(self.request, context)
        context["character"] = self.request.GET["character"]
        general = Character.objects.filter(id=1).get()
        chara = Character.objects.filter(id=self.request.GET["character"]).get()
        context["character_data"] = chara
        context["move_type_list"] = MoveType.objects.filter(character__in=[general,chara]).order_by('order')
        context['move_order_form'] = MoveSortForm(self.request.GET)
        return context


class MoveDetail(DetailView):
    model = Move
    template_name = 'database/move_detail.html'
    context_object_name = "move"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = context_initializer(self.request, context)
        return context



class MoveCreate(CreateView):
    model = Move
    form_class = CreateMoveForm
    template_name = 'database/move_create.html'
    context_object_name = "move"
    #success_url = 'database/move_create/success'
    
    def get_initial(self):
        initial = super().get_initial()
        initial['character'] = self.request.GET.get('character',1)
        return initial

    def form_valid(self,form):
        instance = form.save()
        success_url=f'/database/frame_data/move_list?character={self.request.GET["character"]}'
        return HttpResponseRedirect(success_url)


    def get_form(self,form_class=None):
        form = super().get_form(form_class)
        general = Character.objects.filter(id=1).get()
        chara = Character.objects.filter(id=self.request.GET["character"]).get()
        form.fields['move_type'].queryset = MoveType.objects.filter(character__in=[general,chara])
        form.fields['parent_move'].queryset =  Move.objects.filter(character=chara)
        return form
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = context_initializer(self.request, context)
        return context


class MoveUpdate(UpdateView):
    model = Move
    form_class = UpdateMoveForm
    template_name = 'database/move_update.html'
    success_url = f'/database/move_detail/{{}}'

    def form_valid(self,form):
        instance = form.save()
        success_url=f'/database/frame_data/move_detail/{self.get_object().id}'
        return HttpResponseRedirect(success_url)
    
    def get_form(self,form_class=None):
        form = super().get_form(form_class)
        general = Character.objects.filter(id=1).get()
        chara = self.get_object().character
        form.fields['move_type'].queryset = MoveType.objects.filter(character__in=[general,chara])
        form.fields['parent_move'].queryset =  Move.objects.filter(character=chara)
        return form
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = context_initializer(self.request, context)
        return context


def moveCreateSuccess(request):
    context = {}
    context = context_initializer(this.request, context)
    context["character_list"] = Character.objects.all()
    
    return render(request, "database/index.html", context)


