# This file is to populate some dummy data into the database for testing.
# To do so, run the following command:

# python populate_demo.py
# python manage.py runserver

# Then, go to http://127.0.0.1:8000/admin/
# To gain administrative access, please log in with the following information.

#   Username: admin
#   Password: 123456

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'ltc.settings')

import django

django.setup()
from ltc_main.models import *


def populate_time_period():
    # 5 days a week. Each day from 9:00 to 18:00. Assume each period lasts 1 hour.
    days = [TimePeriod.MON, TimePeriod.TUE, TimePeriod.WED, TimePeriod.THU, TimePeriod.FRI]
    for day in days:
        for time in range(9, 18):
            t = TimePeriod.objects.get_or_create(day=day, time=time)[0]
            t.save()
    return


def populate_user(student_usernames, professor_usernames):
    admin = User.objects.get_or_create(username='admin')[0]
    admin.set_password('123456')
    admin.email = "admin@student.gla.ac.uk"
    admin.is_staff = True
    admin.is_superuser = True
    admin.save()

    for name in student_usernames:
        t = User.objects.get_or_create(username=name)[0]
        # The default email is user's name plus '@student.gla.ac.uk'
        t.email = name + '@student.gla.ac.uk'
        # Students are not staffs
        t.is_staff = False
        # The default password is user's name plus '123'.
        t.set_password(name + '123')
        t.save()

    for name in professor_usernames:
        t = User.objects.get_or_create(username=name)[0]
        t.email = name + '@student.gla.ac.uk'
        t.is_staff = True
        t.set_password(name + '123')
        t.save()
    return


def populate_professor(professor_usernames):
    for name in professor_usernames:
        t = Professor.objects.get_or_create(user=User.objects.get(username=name))[0]
        t.save()
    return


def populate_student(student_usernames):
    for name in student_usernames:
        t = Student.objects.get_or_create(user=User.objects.get(username=name))[0]
        t.save()
    return


def populate_course(courses):
    for course in courses:
        t = Course.objects.get_or_create(name=course['name'])[0]
        t.prerequisite.set([Course.objects.get(name=pre) for pre in course['prerequisite']])
        t.time_period.set([TimePeriod.objects.get(day=day, time=time) for day, time in course['time_period']])
        t.professor = Professor.objects.get_or_create(user=User.objects.get(username=course['professor']))[0]
        t.student.set([Student.objects.get(user=User.objects.get(username=student)) for student in course['student']])
        t.save()
    return


def populate_assignment(assignments):
    for info in assignments:
        try:
            t = Assignment.objects.create(course=Course.objects.get(name=info['course']))
            t.title = info['title']
            t.detail = info['detail']
            t.save()
        except django.db.utils.IntegrityError:
            pass
    return


def populate():
    # Set usernames here.
    # The default email is username plus '@student.gla.ac.uk'
    # The default password is username plus '123'.
    student_usernames = ['Jack', 'Emily']
    professor_usernames = ['Harry', 'Charlotte']

    # Set courses info here.
    courses = [
        {'name': 'course A', 'prerequisite': [], 'time_period': [(TimePeriod.MON, 9)], 'professor': 'Harry',
         'student': ['Jack', ], },
        {'name': 'course B', 'prerequisite': [], 'time_period': [(TimePeriod.MON, 10), (TimePeriod.TUE, 10)],
         'professor': 'Harry', 'student': [], },
        {'name': 'course C', 'prerequisite': ['course B'], 'time_period': [(TimePeriod.MON, 11)],
         'professor': 'Charlotte', 'student': [], },
        {'name': 'course C Hard', 'prerequisite': ['course C', 'course A'], 'time_period': [(TimePeriod.MON, 10)],
         'professor': 'Charlotte', 'student': [], },
    ]

    # Set assignments here.
    assignments = [
        {'course': 'course A', 'title': 'Assignment 01', 'detail': 'Assignment 01 detail.'},
        {'course': 'course A', 'title': 'Assignment 02', 'detail': 'Assignment 02 detail.'},
        {'course': 'course B', 'title': 'Assignment 03', 'detail': 'Assignment 03 detail.'},
    ]

    populate_time_period()
    populate_user(student_usernames, professor_usernames)
    # The Professor points to the User, so the User goes first.
    populate_professor(professor_usernames)
    # The Student points to the User.
    populate_student(student_usernames)
    # The Course points to those above.
    populate_course(courses)
    # The Assignment points to the Course
    populate_assignment(assignments)


if __name__ == '__main__':
    print('Starting MoodlePlus population script...')
    populate()
    print('Done.')
