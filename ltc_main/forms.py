from django import forms
from .models import *


class UserForm(forms.ModelForm):
    STUDENT = 'Student'
    PROFESSOR = Staff.PROFESSOR
    TEACHING_ASSISTANT = Staff.TEACHING_ASSISTANT
    ADMINISTRATOR = Staff.ADMINISTRATOR
    CHOICES = [
        (STUDENT, 'Student'),
        (PROFESSOR, 'Staff - Professor'),
        (TEACHING_ASSISTANT, 'Staff - Teaching assistant'),
        (ADMINISTRATOR, 'Staff - Administrator'),
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

"""
class TimeSlotForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        exclude = ('slug',)
"""

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

class DateInput(forms.DateInput):
    input_type = 'date'

class MeetingForm(forms.ModelForm):
    #name = forms.CharField()
    #members = forms.MultipleChoiceField(widget = forms.HiddenInput, required=False)
    #slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    #id = forms.IntegerField(widget=forms.HiddenInput())
    class Meta:
        model = TeamMeeting
        fields = ['name', 'weekNumber']
        widgets = {
            'made_on': DateInput(),
        }


