import datetime
from django.shortcuts import redirect, render
from django.views import generic
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Sum
from django.utils import timezone
from django.db.models.functions import TruncDay


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
    
def task_stats(request):
    user = User.objects.get(name=request.GET.get('user'))
    # Get the count of open and completed todos
    open_todos = Task.objects.filter(completed=False, user=user).count()
    completed_todos = Task.objects.filter(completed=True).count()

    # Create the data dictionary
    data = {
        'labels': ['Open', 'Completed'],
        'datasets': [{
            'data': [open_todos, completed_todos],
            'backgroundColor': ['#FF6384', '#36A2EB'],
            'hoverBackgroundColor': ['#FF6384', '#36A2EB']
        }]
    }

    return JsonResponse(data)


def tasks_completed_per_day(request):
    user = User.objects.get(name=request.GET.get('user'))
    # Get the count of completed todos per day for the last 7 days
    today = timezone.now()
    last_week = today - datetime.timedelta(days=6)
    completed_per_day = Task.objects.filter(date_completed__date__range=(last_week, today), user=user).annotate(
        date=TruncDay('date_completed')).values('date').annotate(count=Count('id')).order_by('date')

    # Create the data dictionary
    labels = []
    data = []
    for entry in completed_per_day:
        labels.append(entry['date'].strftime('%Y-%m-%d'))
        data.append(entry['count'])

    data = {
        'labels': labels,
        'datasets': [{
            'label': 'Todos Completed',
            'data': data,
            'backgroundColor': '#36A2EB'
        }]
    }

    return JsonResponse(data)

def task_completion_time(request):
    user = User.objects.get(name=request.GET.get('user'))
    # Calculate the time taken to complete tasks
    tasks = Task.objects.filter(completed=True, user=user).exclude(date_completed__isnull=True)
    completion_times = [(task.date_completed - task.date_created).total_seconds() / 3600 for task in tasks]

    # Create the data dictionary
    data = {
        'labels': ['Task Completion Time'],
        'datasets': [{
            'label': 'Average Task Completion Time (hours)',
            'data': completion_times,
            'backgroundColor': '#36A2EB'
        }]
    }

    return JsonResponse(data)

def task_completion_rate(request):
    user = User.objects.get(name=request.GET.get('user'))
    # Calculate the task completion rate
    total_tasks = Task.objects.filter(user=user).count()
    completed_tasks = Task.objects.filter(completed=True, user=user).count()

    # Calculate the completion rate as a percentage
    completion_rate = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

    # Create the data dictionary
    data = {
        'labels': ['Task Completion Rate'],
        'datasets': [{
            'label': 'Task Completion Rate',
            'data': [completion_rate],
            'backgroundColor': '#36A2EB'
        }]
    }

    return JsonResponse(data)

def task_overdue_rate(request):
    total_tasks = Task.objects.count()
    overdue_tasks = Task.objects.filter(completed=False, date_due__lt=timezone.now()).count()

    overdue_rate = (overdue_tasks / total_tasks) * 100 if total_tasks > 0 else 0

    data = {
        'labels': ['Overdue Rate'],
        'datasets': [{
            'label': 'Overdue Rate',
            'data': [overdue_rate],
            'backgroundColor': '#FF6384',
            'borderColor': '#FF6384',
            'fill': False
        }]
    }

    return JsonResponse(data)

def task_creation_rate(request):
    tasks_created_per_day = Task.objects.annotate(date_created_day=TruncDay('date_created')).values('date_created_day').annotate(count=Count('id')).order_by('date_created_day')

    labels = []
    data = []
    for entry in tasks_created_per_day:
        labels.append(entry['date_created_day'].strftime('%Y-%m-%d'))
        data.append(entry['count'])

    data = {
        'labels': labels,
        'datasets': [{
            'label': 'Task Creation Rate',
            'data': data,
            'backgroundColor': 'rgba(54, 162, 235, 0.5)',
            'borderColor': '#36A2EB',
            'fill': True
        }]
    }

    return JsonResponse(data)

    