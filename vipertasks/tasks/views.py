from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse


# Create your views here.
def index(request):
    return HttpResponse("Hello, APL")

class IndexView(generic.ListView):
    template_name = 'tasks/index.html'
    context_object_name = 'task_list'
    