from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    """
    トップ画面のview
    :param request:
    :return:HttpResponse
    """
    return HttpResponse("news index")