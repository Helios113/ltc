from django import forms
from .models import *


class UserForm(forms.ModelForm):
    STUDENT = 'STU'
    PROFESSOR = 'PRO'
    CHOICES = [
        (STUDENT, 'Student'),
        (PROFESSOR, 'Staff'),
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
        exclude = ('slug',)


class TimeSlotForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        exclude = ('slug',)


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ('slug',)


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        exclude = ('slug',)


class DegreeForm(forms.ModelForm):
    class Meta:
        model = Degree
        exclude = ('slug',)
