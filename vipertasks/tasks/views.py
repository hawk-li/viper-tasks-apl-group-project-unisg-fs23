from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse

from .models import Task


# Create your views here.
def index(request):
    # return template from tasks/index.html
    return render(request, 'tasks/index.html')

class IndexView(generic.ListView):
    template_name = 'tasks/tasklist.html'
    context_object_name = 'task_list'
    queryset = Task.objects.all()
    