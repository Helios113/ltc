from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


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
    time = models.IntegerField(default=9)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self))
        super(TimeSlot, self).save(*args, **kwargs)

    class Meta:
        unique_together = (("day", "time"),)

    def __str__(self):
        return self.day + ' ' + str(self.time)


class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self))
        super(Professor, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self))
        super(Student, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user)


class Course(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(max_length=512, null=True)

    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, null=True)
    prerequisite = models.ManyToManyField('self', symmetrical=False, blank=True)
    student = models.ManyToManyField(Student, blank=True)
    time_slot = models.ManyToManyField(TimeSlot, blank=True)

    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self))
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


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
