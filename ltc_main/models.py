from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import math


# Create your models here.


class TimeSlot(models.Model):
    MON = 'MONDAY'
    TUE = 'TUESDAY'
    WED = 'WEDNESDAY'
    THU = 'THURSDAY'
    FRI = 'FRIDAY'

    DayInWeekChoices = (
        (MON, 'Monday'),
        (TUE, 'Tuesday'),
        (WED, 'Wednesday'),
        (THU, 'Thursday'),
        (FRI, 'Friday'),
    )

    day = models.CharField(
        max_length=9,
        choices=DayInWeekChoices,
        default=MON,
    )
    time = models.FloatField(default=9)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self))
        super(TimeSlot, self).save(*args, **kwargs)

    class Meta:
        unique_together = (("day", "time"),)

    def __str__(self):
        # Make time look good.
        minute = int(round(math.modf(self.time)[0] * 60))
        hour = int(math.modf(self.time)[1])
        minute_str = str(minute)
        if minute_str == '0':
            minute_str = '00'
        return self.day.title() + str(hour) + ":" + minute_str


class Staff(models.Model):
    PROF = 'PROFESSOR'
    TA = 'TA'
    ADMIN = 'ADMIN'
    TypeChoices = (
        (PROF, 'Professor'),
        (TA, 'Teaching assistant'),
        (ADMIN, 'Administrator'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(
        max_length=64,
        choices=TypeChoices,
        default=PROF,
    )
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self))
        super(Staff, self).save(*args, **kwargs)

    def get_available_time_slots(self):
        unavailable_time_slots_pks = []
        for course in self.course_set.all():
            for event in course.event_set.all():
                for time_slot in event.time_slot.all():
                    if time_slot.pk not in unavailable_time_slots_pks:
                        unavailable_time_slots_pks.append(time_slot.pk)
        available_time_slots = TimeSlot.objects.exclude(pk__in=unavailable_time_slots_pks)
        return available_time_slots

    def __str__(self):
        return str(self.user)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def get_courses(self):
        courses_pks=[]
        for event in self.event_set.all():
            if event.course.pk not in courses_pks:
                courses_pks.append(event.course.pk)
        courses = Course.objects.filter(pk__in=courses_pks)
        return courses

    def get_available_time_slots(self):
        unavailable_time_slots_pks = []
        for event in self.event_set.all():
            for time_slot in event.time_slot.all():
                if time_slot.pk not in unavailable_time_slots_pks:
                    unavailable_time_slots_pks.append(time_slot.pk)
        available_time_slots = TimeSlot.objects.exclude(pk__in=unavailable_time_slots_pks)
        return available_time_slots

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self))
        super(Student, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user)


class Course(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(max_length=512, null=True)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    prerequisite = models.ManyToManyField('self', symmetrical=False, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self))
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Event(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    student = models.ManyToManyField(Student, blank=True)
    location = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    time_slot = models.ManyToManyField(TimeSlot, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self))
        super(Event, self).save(*args, **kwargs)

    class Meta:
        unique_together = (("course", "name"),)

    def __str__(self):
        return str(self.course) + ' ' + str(self.name)


class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    detail = models.TextField(max_length=512, null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self))
        super(Assignment, self).save(*args, **kwargs)

    class Meta:
        unique_together = (("course", "title"),)

    def __str__(self):
        return str(self.course) + ' ' + self.title


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    result = models.CharField(max_length=128)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self))
        super(Grade, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.pk) + ' ' + str(self.student) + ' ' + str(self.staff) + ' ' + str(self.course)


class Degree(models.Model):
    name = models.CharField(max_length=128, unique=True)
    course = models.ManyToManyField(Course)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self))
        super(Degree, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)
