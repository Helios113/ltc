from django import forms
from .models import *
from datetime import datetime


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

    degree = forms.ModelChoiceField(
        queryset=Degree.objects.all(), required=True,)
    identity = forms.ChoiceField(choices=CHOICES, initial=STUDENT)

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ('username','password','first_name', 'last_name')


class CourseForm(forms.ModelForm):
    endDate = forms.DateField(label='End Date',widget=forms.TextInput(attrs={'type': 'date',}))
    degree = forms.ModelChoiceField(
        queryset=Degree.objects.all(), required=True,)

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Course
        exclude = ('slug', 'photo')


class AssignmentForm(forms.ModelForm):
    deadline = forms.SplitDateTimeField(widget=forms.SplitDateTimeWidget(
        date_attrs={'type': 'date'}, time_attrs={'type': 'time'}))

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Assignment
        exclude = ('slug', 'course')


class EventForm(forms.ModelForm):
    start = forms.SplitDateTimeField(widget=forms.SplitDateTimeWidget(
        date_attrs={'type': 'date'}, time_attrs={'type': 'time'}), required=True)

    end = forms.SplitDateTimeField(widget=forms.SplitDateTimeWidget(
        date_attrs={'type': 'date'}, time_attrs={'type': 'time'}), required=True)
    # EVENTTOOLS_REPEAT_CHOICES = (
    #     ("RRULE:FREQ=DAILY", 'Daily'),
    #     ("RRULE:FREQ=WEEKLY", 'Weekly'),
    #     ("RRULE:FREQ=MONTHLY", 'Monthly'),
    #     ("RRULE:FREQ=YEARLY", 'Yearly'),
    # )
    # repeat = forms.ChoiceField(
    #     choices=EVENTTOOLS_REPEAT_CHOICES, required=False)
    repeat_until = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date'}), required=False)

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Event
        exclude = ('slug', 'course', 'type')


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

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = TeamMeeting
        fields = ['name', 'weekNumber']
        widgets = {
            'made_on': DateInput(),
        }

def make_grading_form(assignment):
    """
    Returns a grading form for the given assignment, 
    restricting the student choices to those in the 
    course's atendees. 
    """
    class GradingForm(forms.ModelForm):
        student = forms.ModelChoiceField(queryset=Student.objects.filter(courses=assignment.course))
        def __init__(self, *args, **kwargs):
            super(forms.ModelForm, self).__init__(*args, **kwargs)
            for visible in self.visible_fields():
                visible.field.widget.attrs['class'] = 'form-control'

        class Meta:
            model = Grade
            exclude=('course', 'assignment')
    return GradingForm
