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
        "LP":0,
        "RP":1,
        "LK":2,
        "RK":3,
        "WP":4,
        "WK":5,
        "【":6,
        "641236":22,
        "6n23":21,
        "666":18,
        "66_":17,
        "6n":16,
        "6":7,
        "3":8,
        "236":20,
        "2":9,
        "1":10,
        "44":19,
        "4":11,
        "7":12,
        "8":13,
        "9":14,
        "9n":15,
        "立ち途中に":23,
        "しゃがんだ状態で":24,
        "ヒート発動可能状態で":25,
        "ヒート状態で":26,
        "レイジ状態で":27,
        "横移動中に":28,
        "相手に接近して":29,
        "相手の左側面から接近して":30,
        "相手の右側面から接近して":31,
        "相手の背後から接近して":32,
        "(相手ダウン中に)":33,
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


