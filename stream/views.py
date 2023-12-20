from django.shortcuts import render
from top.util.page_initializer import context_initializer
from .form import StreamSearchForm,StreamSortForm
from django.http import JsonResponse,HttpResponse
import redis

# Create your views here.


def index(request):
    """
    TEKKEN MANIAXのStream機能表示用View
    :param request:
    :return:
    """


    context = {}
    context = context_initializer(request, context)
    context['search_form'] = StreamSearchForm(request.GET)
    context['search_order_form'] = StreamSortForm(request.GET)
    return render(request, "stream/index.html", context)

def list_stream_endpoint(request):
    print("List_stream_endpoint:アクセスされてます")
    return JsonResponse({})
