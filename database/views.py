##
##database/views.py
##

from django.shortcuts import render
from top.util.page_initializer import context_initializer

def index(request):
    """
    TEKKEN MANIAXのデータベースページの表示用View
    :param request:
    :return:
    """
    context = {}
    context = context_initializer(request, context)
    return render(request, "database/index.html", context)
# Create your views here.
