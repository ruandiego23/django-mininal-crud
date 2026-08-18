from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from webdev.tasks.forms import TaskNewForm, TaskForm
from webdev.tasks.models import Task


# Create your views here.
def home(request):
    if request.method == 'POST':
        form = TaskNewForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('tasks:home'))
        else:
            pending_tasks = Task.objects.filter(done=False).all()
            return render(request, 'tasks/home.html', {'form': form, 'pending_tasks': pending_tasks}, status=400)
    pending_tasks = Task.objects.filter(done=False).all()
    return render(request, 'tasks/home.html', {'pending_tasks': pending_tasks})


def detail(request, task_id):
    if request.method == 'POST':
        task = Task.objects.get(id=task_id)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
    return HttpResponseRedirect(reverse('tasks:home'))
