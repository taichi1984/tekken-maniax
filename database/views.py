##
##database/views.py
##

from django.shortcuts import render
from django.db.models import IntegerField,CharField, Value, Case, When, F
from top.util.page_initializer import context_initializer
from guide.models import Character
from django.views.generic import ListView,DetailView,CreateView,UpdateView
from .models import Move
from .form import CreateMoveForm,UpdateMoveForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
import re
from django.urls import reverse

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
        "66":17,
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
        "横移動中に":25,
        "相手に接近して":26,
        "相手の左側面から接近して":27,
        "相手の右側面から接近して":28,
        "相手の背後から接近して":29,
        "相手ダウン中に":30,
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

        for query in queryset:
            parent_move = query.parent_move
            full_command_jp = query.command_jp

            while parent_move:
                full_command_jp = f"{parent_move.command_jp} > {full_command_jp}"
                parent_move = parent_move.parent_move
            
            query.full_command_jp = full_command_jp
        
        
        sorted_queryset = sorted(queryset,key=custom_order_key)

        return sorted_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = context_initializer(self.request, context)
        context["character"] = self.request.GET["character"]
        return context


class MoveDetail(DetailView):
    model = Move
    template_name = 'database/move_detail.html'
    context_object_name = "move"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = context_initializer(self.request, context)



class MoveCreate(CreateView):
    model = Move
    form_class = CreateMoveForm
    template_name = 'database/move_create.html'
    context_object_name = "move"
    #success_url = 'database/move_create/success'
    

    def form_valid(self,form):
        instance = form.save()
        success_url=f'/database/move_list?character={self.request.GET["character"]}'
        return HttpResponseRedirect(success_url)


    def get_form(self,form_class=None):
        form = super().get_form(form_class)
        chara = Character.objects.filter(id=self.request.GET["character"]).get()
        form.fields['parent_move'].queryset =  Move.objects.filter(character=chara)
        return form
    
    


class MoveUpdate(UpdateView):
    model = Move
    form_class = UpdateMoveForm
    template_name = 'database/move_update.html'
    success_url = f'/database/move_detail/{{}}'

    def form_valid(self,form):
        instance = form.save()
        success_url=f'/database/move_detail/{self.get_object().id}'
        return HttpResponseRedirect(success_url)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = context_initializer(self.request, context)


def moveCreateSuccess(request):
    context = {}
    context = context_initializer(this.request, context)
    context["character_list"] = Character.objects.all()
    
    return render(request, "database/index.html", context)


