from django import forms
from webdev.tasks.models import Task


class TaskNewForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = 'name',
