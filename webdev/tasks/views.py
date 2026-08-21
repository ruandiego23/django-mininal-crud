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
            done_tasks = Task.objects.filter(done=True).all()
            return render(
                request, 'tasks/home.html',
                {
                    'form': form,
                    'pending_tasks': pending_tasks,
                    'done_tasks': done_tasks,
                 },
                status=400
            )
    pending_tasks = Task.objects.filter(done=False).all()
    done_tasks = Task.objects.filter(done=True).all()
    return render(
        request,
        'tasks/home.html',
        {
            'pending_tasks': pending_tasks,
            'done_tasks': done_tasks,
        }
    )


def detail(request, task_id):
    if request.method == 'POST':
        task = Task.objects.get(id=task_id)

        # 1. Create a mutable copy of the POST data
        data = request.POST.copy()

        # 2. Check the custom task_status flag we added to the HTML
        task_status = data.get('task_status')
        if task_status == 'complete':
            data['done'] = 'True'
        elif task_status == 'pending':
            data['done'] = 'False'

        # 3. Pass the modified data to your TaskForm
        form = TaskForm(data, instance=task)
        if form.is_valid():
            form.save()
    return HttpResponseRedirect(reverse('tasks:home'))


def erase(request, task_id):
    if request.method == 'POST':
        Task.objects.filter(id=task_id).delete()
    return HttpResponseRedirect(reverse('tasks:home'))
