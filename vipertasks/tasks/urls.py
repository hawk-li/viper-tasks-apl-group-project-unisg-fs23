from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:user_name>/tasks', views.IndexView, name='user'),
    path('task', views.add_task, name='add_task'),
    path('task/complete', views.complete_task, name='complete_task'),
    path('task/completed_count', views.completed_task_count, name='completed_todos_count')
]