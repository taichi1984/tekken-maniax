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
        "LP+RK":510,
        "RP+LK":520,
        "LP":50,
        "RP":100,
        "LK":200,
        "RK":300,
        "WP":400,
        "WK":500,
        "【":600,
        "641236":2200,
        "6n23":2100,
        "44_":1750,
        "666_":1800,
        "66_":1700,
        "6n":1600,
        "6LP+RK":770,
        "6RP+LK":780,
        "6LP":710,
        "6RP":720,
        "6LK":730,
        "6RK":740,
        "6WP":750,
        "6WK":760,
        "6":790,
        "3LP+RK":870,
        "3RP+LK":880,
        "3LP":810,
        "3RP":820,
        "3LK":830,
        "3RK":840,
        "3WP":850,
        "3WK":860,
        "3":890,
        "236":2000,
        "2LP+RK":970,
        "2RP+LK":980,
        "2LP":910,
        "2RP":920,
        "2LK":930,
        "2RK":940,
        "2WP":950,
        "2WK":960,
        "2":990,
        "1LP+RK":1070,
        "1RP+LK":1080,
        "1LP":1010,
        "1RP":1020,
        "1LK":1030,
        "1RK":1040,
        "1WP":1050,
        "1WK":1060,
        "1":1090,
        "44_":1900,
        "4LP+RK":1160,
        "4RP+LK":1170,
        "4LP":1100,
        "4RP":1110,
        "4LK":1120,
        "4RK":1130,
        "4WP":1140,
        "4WK":1150,
        "4":1180,
        "7LP+RK":1270,
        "7RP+LK":1280,
        "7LP":1210,
        "7RP":1220,
        "7LK":1230,
        "7RK":1240,
        "7WP":1250,
        "7WK":1260,
        "7":1290,
        "8LP":1310,
        "8RP":1320,
        "8LK":1330,
        "8RK":1340,
        "8WP":1350,
        "8WK":1360,
        "8LP+RK":1370,
        "8RP+LK":1380,
        "8":1390,
        "9LP+RK":1470,
        "9RP+LK":1480,
        "9LP":1410,
        "9RP":1420,
        "9LK":1430,
        "9RK":1440,
        "9WP":1450,
        "9WK":1460,
        "9":1470,
        "9n":1500,
        "46":1550,
        "走り中に":2250,
        "立ち途中に":2300,
        "しゃがんだ状態で":2400,
        "ヒート状態で":2600,
        "レイジ状態で":2700,
        "横移動中に":2800,
        "相手に接近して":2900,
        "(相手しゃがみ中に)":2950,
        "(相手壁やられ中に)":2960,
        "相手の左側面から接近して":3000,
        "相手の右側面から接近して":3100,
        "相手の背後から接近して":3200,
        "(相手ダウン中に)":3300,
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


