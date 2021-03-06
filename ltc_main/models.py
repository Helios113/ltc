import imp
from statistics import mode
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.core.files import File
from django import forms
import ltc_main.image_generator as ig
import math
import uuid
import datetime
from eventtools.models import BaseEvent, BaseOccurrence


# Create your models here.

class Staff(models.Model):
    # There are three types of choice for staff, Professor, Teaching assistant and Administrator
    PROFESSOR = 'Professor'
    TEACHING_ASSISTANT = 'Teaching assistant'
    ADMINISTRATOR = 'Administrator'
    TypeChoices = (
        (PROFESSOR, 'Professor'),
        (TEACHING_ASSISTANT, 'Teaching assistant'),
        (ADMINISTRATOR, 'Administrator'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)
    # Time slots should be calculated.
    # If you want to get someone's time slots, calculate them dynamically by function rather than storing them AGAIN.
    # Or it would be hard to maintain the time slots when the time of an event changes.
    courses = models.ManyToManyField('Course')
    type = models.CharField(
        max_length=64,
        choices=TypeChoices,
        default=PROFESSOR,
    )

    def get_time_slots(self):
        t = []
        for course in self.courses.all():
            for event in course.event_set.all():
                t.append(event)
        pks = [i.pk for i in t]
        return Event.objects.filter(pk__in=pks)

    def get_assignments(self):
        a = []
        for course in self.courses.all():
            for assignment in course.assignment_set.all():
                a.append(assignment)
        return a

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self))
        super(Staff, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user)


class Course(models.Model):
    # One courses can be enrolled by many students, courses have events like lab, tutorials and labs with time slots,
    # Some courses may have request for relative prerequisite
    code = models.CharField(max_length=128, unique=True)
    endDate = models.DateField(default=datetime.date.today())
    name = models.CharField(max_length=128, default='default')
    description = models.TextField(max_length=512, default='default')
    prerequisite = models.ManyToManyField(
        'self', symmetrical=False, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    photo = models.TextField()

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self))
        # Auto-generate the icon for course
        self.photo = ig.generate_identicon(self.name)
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.code + ' ' + self.name


class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    detail = models.TextField(max_length=512, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    deadline = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self))
        super(Assignment, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.course.code) + ' ' + self.title


class Grade(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE)
    result = models.IntegerField(default=0)


class Degree(models.Model):
    name = models.CharField(max_length=128, unique=True)
    course = models.ManyToManyField(Course)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self))
        super(Degree, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)


class Event(BaseOccurrence):
    # A course can have many events, and there are 3 types of events: lab, tutorials and lectures, a map or a zoom links
    # will be auto-generated when clicked the concreate event page
    course = models.ForeignKey(Course, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=512, null=True)
    location = models.CharField(max_length=128)
    geoUri = models.CharField(
        max_length=128, default="geo:55.8726,-4.2896?z=16")
    lecture = 'Lecture'
    tutorial = 'Tutorial'
    lab = 'Lab'
    TypeChoices = (
        (lecture, 'Lecture'),
        (tutorial, 'Tutorial'),
        (lab, 'Lab'),
    )
    type = models.CharField(
        max_length=64,
        choices=TypeChoices,
        default=lecture,
    )
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self))
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.course.name+"-"+self.name)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, null=True, blank=True)

    # Students attend courses, courses have events with time slots, so students' time slots can be calculated.
    # If you want to get someone's time slots, calculate them dynamically by function rather than storing them AGAIN.
    # Or it would be hard to maintain the time slots when the time of an event changes.
    def get_time_slots(self):
        t = []
        for course in self.courses.all():
            for event in course.event_set.all():
                t.append(event)
        pks = [i.pk for i in t]
        return Event.objects.filter(pk__in=pks)

    courses = models.ManyToManyField(Course, blank=True)

    def get_assignments(self):
        a = []
        for course in self.courses.all():
            for assignment in course.assignment_set.all():
                a.append(assignment)
        return a

    degree = models.ForeignKey(Degree, null=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self))
        super(Student, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user)


class TeamMeeting(models.Model):
    # User can select the team members to arrange a team meeting, they are allowed to have a team meeting
    # in different week. Finding the available timeslots among all members and name the meeting
    thisWeek = datetime.date.today().isocalendar()[1]
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owner", null=True)
    members = models.ManyToManyField(User, blank=True)
    name = models.CharField(max_length=128, blank=False)
    slug = models.SlugField(unique=True, editable=False, null=True, blank=True)
    choices = zip(range(thisWeek, 53), [str(e) for e in range(thisWeek, 53)])
    weekNumber = models.IntegerField(
        'Week Number', choices=choices, default=thisWeek)

    #This is intentional
    def saveSlug(self, *args, **kwargs):
        self.slug = slugify(str(self))
        super(TeamMeeting, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id) + self.name
