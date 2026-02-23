from django.urls import path
from .views import TaskListView, TaskCreateView, TaskDetailView, TaskUpdateView, InactiveTaskListView

app_name = 'tasks'

urlpatterns = [
    path("", TaskListView.as_view(), name="task_list"),
    path("create/", TaskCreateView.as_view(), name="task_create"),
    path("<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
    path('<int:pk>/edit/', TaskUpdateView.as_view(), name='task_edit'),
    path("inactives/", InactiveTaskListView.as_view(), name="inactive_tasks"),
]