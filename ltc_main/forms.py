from django import forms
from django.contrib.auth.models import User
from .models import *


class UserForm(forms.ModelForm):
    STUDENT = 'STU'
    PROFESSOR = 'PRO'
    CHOICES = [
        (STUDENT, 'Student'),
        (PROFESSOR, 'Professor'),
    ]
    password = forms.CharField(widget=forms.PasswordInput())
    identity = forms.ChoiceField(choices=CHOICES, initial=STUDENT)

    class Meta:
        model = User
        fields = ('username', 'password',)


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        exclude = ('slug',)


class AssignmentForm(forms.ModelForm):

    class Meta:
        model = Assignment
        exclude = ()
