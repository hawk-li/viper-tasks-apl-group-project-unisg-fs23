from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:user_name>/tasks', views.IndexView, name='user'),
    path('task', views.add_task, name='add_task'),
    path('task/complete', views.complete_task, name='complete_task'),
    path('task/delete', views.delete_task, name='delete_task'),
    path('task/stats', views.task_stats, name='task_stats'),
    path('task/completed-per-day', views.tasks_completed_per_day, name='tasks_completed_per_day'),
    path('task/completion-time', views.task_completion_time, name='task_completion_time'),
    path('task/completion-rate/', views.task_completion_rate, name='task_completion_rate'),
    path('task/overdue-rate/', views.task_overdue_rate, name='task_overdue_rate'),
    path('task/creation-rate/', views.task_creation_rate, name='task_creation_rate'),
]