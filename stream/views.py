from django.shortcuts import render
from top.util.page_initializer import context_initializer

# Create your views here.
def index(request):
    """
    TEKKEN MANIAXのStream機能表示用View
    :param request:
    :return:
    """
    context = {}
    context = context_initializer(request, context)
    return render(request, "stream/index.html", context)