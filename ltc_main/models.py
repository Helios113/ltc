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
    timeSlots = models.ManyToManyField('TimeSlot')
    courses = models.ManyToManyField('Course')
    #assignment = models.ManyToManyField('Assignment',null=True)
    type = models.CharField(
        max_length=64,
        choices=TypeChoices,
        default=PROFESSOR,
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self))
        super(Staff, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user)


class Course(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(max_length=512, null=True)
    prerequisite = models.ManyToManyField(
        'self', symmetrical=False, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    photo = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self))
        self.photo = ig.generate_identicon(self.name)
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.code+' '+self.name


class Assignment(models.Model):
    id = models.IntegerField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    detail = models.TextField(max_length=512, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    deadline = models.OneToOneField(
        'TimeSlot', null=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self))
        super(Assignment, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.course) + ' ' + self.title


class Grade(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE)
    result = models.IntegerField(max_length=3)


class Degree(models.Model):
    name = models.CharField(max_length=128, unique=True)
    course = models.ManyToManyField(Course)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self))
        super(Degree, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)


class Event(BaseEvent):
    id = models.IntegerField(primary_key=True)
    course = models.ForeignKey(Course, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=512, null=True)
    location = models.CharField(max_length=128)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self))
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)


class TimeSlot(BaseOccurrence):
    event = models.ForeignKey(Event, null=True, on_delete=models.CASCADE)


class Student(models.Model):
    #id = models.IntegerField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, null=True, blank=True)
    timeSlots = models.ManyToManyField(TimeSlot, null=True, blank=True)
    courses = models.ManyToManyField(Course, null=True, blank=True)
    assignment = models.ManyToManyField(Assignment, null=True, blank=True)
    degree = models.ForeignKey(Degree, null=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self))
        super(Student, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user)


class TeamMeeting(models.Model):
    thisWeek = datetime.date.today().isocalendar()[1]
    members = models.ManyToManyField(User, blank=True)
    name = models.CharField(max_length=128, blank=False)
    slug = models.SlugField(unique=True, editable=False, null=True, blank=True)
    choices = zip(range(thisWeek, 53), [str(e) for e in range(thisWeek, 53)])
    weekNumber = models.IntegerField(
        'Week Number', choices=choices, default=thisWeek)

    def saveSlug(self, *args, **kwargs):
        self.slug = slugify(str(self))
        super(TeamMeeting, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)+self.name
