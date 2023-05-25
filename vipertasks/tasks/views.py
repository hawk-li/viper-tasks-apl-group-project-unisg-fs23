import datetime
from django.shortcuts import redirect, render
from django.views import generic
from django.http import HttpResponse, JsonResponse

from .models import Task, User


# Create your views here.
def index(request):
    # return template from tasks/index.html
    return render(request, 'tasks/index.html')

def IndexView(request, user_name):
    # extract user name from url
    user_name = request.path.split('/')[1]
    # get or create user
    user, created = User.objects.get_or_create(name=user_name)
    # get user id


    template_name = 'tasks/tasklist.html'
    context_object_name = 'task_list'
    queryset = Task.objects.filter(user=user.id).order_by('date_due')

    return render(request, template_name, {'task_list': queryset})

def add_task(request):
    if request.method == 'POST':
        # Extract data from the POST request
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        completed = request.POST.get('completed') == 'on'  # Convert checkbox value to boolean
        user = request.POST.get('user')

        # Get the user object
        user = User.objects.get(name=user)

        # Create a new task object
        task = Task(name=title, description=description, date_due=due_date, completed=completed, user=user)
        task.save()

        # Redirect to a success page or a task list page
        return redirect('/' + user.name + '/tasks')
    
def complete_task(request):
    if request.method == 'POST':
        # Extract data from the POST request
        task_id = request.POST.get('task_id')
        task = Task.objects.get(id=task_id)
        task.completed = True
        task.date_completed = datetime.datetime.now()
        task.save()
        return redirect('/' + task.user.name + '/tasks')
    
def delete_task(request):
    if request.method == 'GET':
        # Extract data from the POST request
        task_id = request.GET.get('task_id')
        user = Task.objects.get(id=task_id).user
        task = Task.objects.get(id=task_id)
        task.delete()
        return redirect('/' + user.name + '/tasks')
    
def completed_task_count(request):
    days = request.GET.get('days')
    user = request.GET.get('user')
    user = User.objects.get(name=user)
    
    today = datetime.datetime.now()
    date_threshold = today - datetime.timedelta(days=int(days))

    completed_count = Task.objects.filter(completed=True, date_completed__gte=date_threshold).count()

    response_data = {
        'completed_count': completed_count,
        'days': days
    }
    
    return JsonResponse(response_data)
    