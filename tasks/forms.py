from django.forms import ModelForm
from .models import task
from django.contrib.auth.forms import UserCreationForm
from django import forms

class TaskForm(ModelForm):
    class Meta:
        model = task
        fields = ['titulo', 'descripcion', 'importante']

class MyUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Nombre de usuario'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Contraseña'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Repite la contraseña'})
