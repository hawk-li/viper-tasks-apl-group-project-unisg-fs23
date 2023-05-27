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
    # Render the tasks/index.html template
    return render(request, 'tasks/index.html')

def IndexView(request, user_name):
    # Extract user name from URL
    user_name = request.path.split('/')[1]
    # Get or create user based on the extracted user name
    user, created = User.objects.get_or_create(name=user_name)
    
    # Set the template and context object names
    template_name = 'tasks/tasklist.html'
    context_object_name = 'task_list'
    
    # Query the tasks for the user and order them by due date
    queryset = Task.objects.filter(user=user.id).order_by('date_due')

    # Render the template with the task list as the context
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

        # Redirect to the task list page for the corresponding user
        return redirect('/' + user.name + '/tasks')

def complete_task(request):
    if request.method == 'POST':
        # Extract data from the POST request
        task_id = request.POST.get('task_id')
        task = Task.objects.get(id=task_id)
        
        # Mark the task as completed and set the completion date
        task.completed = True
        task.date_completed = datetime.datetime.now()
        task.save()
        
        # Redirect to the task list page for the associated user
        return redirect('/' + task.user.name + '/tasks')

def delete_task(request):
    if request.method == 'GET':
        # Extract data from the GET request
        task_id = request.GET.get('task_id')
        user = Task.objects.get(id=task_id).user
        task = Task.objects.get(id=task_id)
        
        # Delete the task
        task.delete()
        
        # Redirect to the task list page for the user associated with the deleted task
        return redirect('/' + user.name + '/tasks')

def task_stats(request):
    # Get the user from the GET request
    user = User.objects.get(name=request.GET.get('user'))
    
    # Get the count of open and completed todos for the user
    open_todos = Task.objects.filter(completed=False, user=user).count()
    completed_todos = Task.objects.filter(completed=True).count()

    # Create the data dictionary for the JSON response
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
    # Get the user from the GET request
    user = User.objects.get(name=request.GET.get('user'))
    
    # Calculate the count of completed todos per day for the last 7 days
    today = timezone.now()
    last_week = today - datetime.timedelta(days=6)
    completed_per_day = Task.objects.filter(date_completed__date__range=(last_week, today), user=user).annotate(
        date=TruncDay('date_completed')).values('date').annotate(count=Count('id')).order_by('date')

    # Create the data dictionary for the JSON response
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
    # Get the user from the GET request
    user = User.objects.get(name=request.GET.get('user'))
    
    # Calculate the time taken to complete tasks for the user
    tasks = Task.objects.filter(completed=True, user=user).exclude(date_completed__isnull=True)
    completion_times = [(task.date_completed - task.date_created).total_seconds() / 3600 for task in tasks]

    # Create the data dictionary for the JSON response
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
    # Get the user from the GET request
    user = User.objects.get(name=request.GET.get('user'))
    
    # Calculate the task completion rate for the user
    total_tasks = Task.objects.filter(user=user).count()
    completed_tasks = Task.objects.filter(completed=True, user=user).count()

    # Calculate the completion rate as a percentage
    completion_rate = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

    # Create the data dictionary for the JSON response
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
    user = User.objects.get(name=request.GET.get('user'))
    # Calculate the total number of tasks
    total_tasks = Task.objects.filter(user=user, completed=False).count()
    
    # Calculate the number of overdue tasks
    overdue_tasks = Task.objects.filter(completed=False, date_due__lt=timezone.now()).count()

    # Calculate the overdue rate as a percentage
    overdue_rate = (overdue_tasks / total_tasks) * 100 if total_tasks > 0 else 0

    # Create the data dictionary for the JSON response
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
    # Calculate the count of tasks created per day
    tasks_created_per_day = Task.objects.annotate(date_created_day=TruncDay('date_created')).values('date_created_day').annotate(count=Count('id')).order_by('date_created_day')

    labels = []
    data = []
    for entry in tasks_created_per_day:
        labels.append(entry['date_created_day'].strftime('%Y-%m-%d'))
        data.append(entry['count'])

    # Create the data dictionary for the JSON response
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