# This file is to populate some dummy data into the database for testing.
# To do so, run the following command:

# python populate_ltc.py
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


def populate_time_slot():
    # 5 days a week. Each day from 9:00 to 18:00. Assume each period lasts 1 hour.
    days = [TimeSlot.MON, TimeSlot.TUE, TimeSlot.WED, TimeSlot.THU, TimeSlot.FRI]
    for day in days:
        for time in range(9, 18):
            t = TimeSlot.objects.get_or_create(day=day, time=time)[0]
            t.save()
    return


def populate_user(student_usernames, professor_usernames):
    # Set up superuser account.
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
        t.professor = Professor.objects.get_or_create(user=User.objects.get(username=course['professor']))[0]
        t.description = course['description']

        t.prerequisite.set([Course.objects.get(name=pre) for pre in course['prerequisite']])
        t.time_slot.set([TimeSlot.objects.get(day=day, time=time) for day, time in course['time_slot']])
        t.student.set([Student.objects.get(user=User.objects.get(username=student)) for student in course['student']])
        t.save()
    return


def populate_assignment(assignments):
    for info in assignments:
        t = Assignment.objects.create(course=Course.objects.get(name=info['course']), title=info['title'])
        t.detail = info['detail']
        t.save()
    return


def populate():
    # Set usernames here.
    # The default email is username plus '@student.gla.ac.uk'
    # The default password is username plus '123'.
    student_usernames = ['Amelia', 'Emily', 'Jack', 'Mason', ]
    professor_usernames = ['Charlotte', 'Harry', ]

    # Set courses info here.
    courses = [
        {'name': 'course A', 'prerequisite': [], 'description':'course A description', 'time_slot': [(TimeSlot.MON, 9), (TimeSlot.MON, 10)], 'professor': 'Harry',
         'student': ['Amelia', 'Jack', ], },
        {'name': 'course B', 'prerequisite': [], 'description':'course B description', 'time_slot': [(TimeSlot.MON, 10), (TimeSlot.TUE, 10)],
         'professor': 'Harry', 'student': ['Amelia', 'Emily', 'Mason', ], },
        {'name': 'course C', 'prerequisite': ['course B'], 'description':'course C description', 'time_slot': [(TimeSlot.MON, 11)],
         'professor': 'Charlotte', 'student': ['Amelia', 'Emily', ], },
        {'name': 'course C Hard', 'prerequisite': ['course A', 'course C'], 'description':'course C Hard description', 'time_slot': [(TimeSlot.MON, 12), (TimeSlot.MON, 13), (TimeSlot.MON, 15)],
         'professor': 'Charlotte', 'student': ['Amelia', ], },
    ]

    # Set assignments here.
    assignments = [
        {'course': 'course A', 'title': 'Assignment 01', 'detail': 'Assignment 01 detail.'},
        {'course': 'course A', 'title': 'Assignment 02', 'detail': 'Assignment 02 detail.'},
        {'course': 'course B', 'title': 'Assignment 03', 'detail': 'Assignment 03 detail.'},
        {'course': 'course C', 'title': 'Assignment 04', 'detail': 'Assignment 04 detail.'},
        {'course': 'course C Hard', 'title': 'Assignment 05', 'detail': 'Assignment 05 detail.'},
        {'course': 'course C Hard', 'title': 'Assignment 06', 'detail': 'Assignment 06 detail.'},
    ]

    populate_time_slot()
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
