from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.urls import reverse

from .models import Task
from .forms import TaskForm


class BaseTaskListView(ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"
    paginate_by = 7
    page_type = None  # перевизначається в дочірніх класах

    def get_queryset(self):
        queryset = self.model.objects.order_by("-created_at")

        if self.page_type == "active":
            queryset = queryset.filter(is_active=True).exclude(
                status=Task.Status.CLOSED
            )

        elif self.page_type == "inactive":
            queryset = queryset.filter(is_active=False).exclude(
                status=Task.Status.CLOSED
            )

        elif self.page_type == "closed":
            queryset = queryset.filter(status=Task.Status.CLOSED)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_type'] = self.page_type

        if self.page_type == "inactive":
            context["back_url"] = reverse("tasks:inactive_tasks")
        elif self.page_type == "closed":
            context["back_url"] = reverse("tasks:closed_tasks")
        else:
            context["back_url"] = reverse("tasks:task_list")

        return context


class TaskListView(BaseTaskListView):
    page_type = "active"


class InactiveTaskListView(BaseTaskListView):
    page_type = "inactive"


class ClosedTaskListView(BaseTaskListView):
    page_type = "closed"


class TaskDetailView(DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page_type = self.request.GET.get("tab", "active")
        context["page_type"] = page_type

        if page_type == "inactive":
            context["back_url"] = reverse("tasks:inactive_tasks")
        elif page_type == "closed":
            context["back_url"] = reverse("tasks:closed_tasks")
        else:
            context["back_url"] = reverse("tasks:task_list")

        return context


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks:task_list")


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_type"] = self.request.GET.get("tab", "active")
        return context

    def get_success_url(self):
        tab = self.request.GET.get("tab", "active")
        return reverse('tasks:task_detail', kwargs={'pk': self.object.pk}) + f'?tab={tab}'
