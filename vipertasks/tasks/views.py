from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse

from .models import Task, User


# Create your views here.
def index(request):
    # return template from tasks/index.html
    return render(request, 'tasks/index.html')

def IndexView(request):
    # extract user name from url
    user_name = request.path.split('/')[1]
    # get or create user
    user = User.objects.get_or_create(name=user_name)

    template_name = 'tasks/tasklist.html'
    context_object_name = 'task_list'
    queryset = Task.objects.filter(user=user)

# accept post request to create new task
def add_task(request):
    # get data from request
    name = request.POST['name']
    description = request.POST['description']
    date_due = request.POST['date_due']
    completed = request.POST['completed']
    # create new task
    new_task = Task(name=name, description=description, date_due=date_due, completed=completed)
    # save task
    new_task.save()
    # return http 200
    return HttpResponse(status=200)
    