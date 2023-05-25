from django.shortcuts import redirect, render
from django.views import generic
from django.http import HttpResponse

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
    queryset = Task.objects.filter(user=user.id)

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

    # Render the add task form if it's a GET request
    #return render(request, 'add_task.html')
    