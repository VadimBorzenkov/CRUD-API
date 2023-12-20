from django import forms
from todo.models import Todo


class Form(forms.ModelForm):
    class Meta:
        model = Todo
        fields = '__all__'
    widgets = {
        'title': forms.TextInput(attrs={'required': False}),
        'description': forms.Textarea(attrs={'required': False}),
        'completed': forms.CheckboxInput(attrs={'required': False}),
    }


class EditForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = '__all__'
