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
from datetime import datetime


def populate_user(student_usernames, staff_usernames):
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

    for name in staff_usernames:
        s = User.objects.get_or_create(username=name)[0]
        s.email = name + '@student.gla.ac.uk'
        s.is_staff = True
        s.set_password(name + '123')
        s.save()
    return


def populate_staff(staffs_info):
    for info in staffs_info:
        s = Staff.objects.get_or_create(user=User.objects.get(username=info['name']))[0]
        s.courses.set(Course.objects.filter(name__in=info['courses']))
        s.type = info['type']
        s.save()
    return


def populate_student(students_info):
    for info in students_info:
        t = Student.objects.get_or_create(user=User.objects.get(username=info['name']))[0]
        t.courses.set(Course.objects.filter(name__in=info['courses']))
        t.degree = Degree.objects.get(name=info['degree'])
        t.save()
    return


def populate_course(courses_info):
    for info in courses_info:
        t = Course.objects.get_or_create(code=info['code'])[0]
        t.name = info['name']
        t.description = info['description']
        t.prerequisite.set(Course.objects.filter(name__in=info['prerequisite']))
        t.save()
    return


def populate_assignment(assignments_info):
    for info in assignments_info:
        t = Assignment.objects.get_or_create(course=Course.objects.get(name=info['course']), title=info['title'])[0]
        t.detail = info['detail']
        t.deadline = datetime(*info['deadline'])
        t.save()
    return


def populate_grade(grades_info):
    for info in grades_info:
        g = Grade.objects.get_or_create(student=Student.objects.get(user=User.objects.get(username=info['student'])),
                                        course=Course.objects.get(name=info['course']),
                                        assignment=Assignment.objects.get(title=info['assignment']))[0]
        g.result = info['result']
        g.save()
    return


def populate_degree(degrees_info):
    for info in degrees_info:
        d = Degree.objects.get_or_create(name=info['name'])[0]
        d.course.set(Course.objects.filter(name__in=info['courses']))
        d.save()
    return


def populate_event(events_info):
    for info in events_info:
        e = Event.objects.get_or_create(id=info['id'])[0]
        e.course = Course.objects.get(name=info['course'])
        e.name = info['name']
        e.description = info['description']
        e.location = info['location']
        e.type = info['type']
        e.save()
    return


def populate_time_slot(time_slots_info):
    for info in time_slots_info:
        t = TimeSlot.objects.get_or_create(
            event=Event.objects.get(id=info['event']),
            start=datetime(*info['from']),
            end=datetime(*info['to']),
            repeat='RRULE:FREQ=WEEKLY'
        )[0]
        t.save()
    return


def populate():
    # Set usernames here.
    # The default email is username plus '@student.gla.ac.uk'
    # The default password is username plus '123'.
    student_usernames = ['Amelia', 'Emily', 'Jack', 'Mason', ]
    staff_usernames = ['Charlotte', 'Harry', ]
    staffs_info = [{'name': 'Charlotte', 'type': Staff.PROFESSOR, 'courses': ['course A', 'course B']},
                   {'name': 'Harry', 'type': Staff.TEACHING_ASSISTANT, 'courses': ['course C', 'course C Hard']}]
    students_info = [
        {
            'name': 'Amelia', 'courses': ['course A', 'course B', 'course C', 'course C Hard'],
            'degree': 'Business Administration and Management',
        },
        {
            'name': 'Emily', 'courses': ['course A', 'course B'], 'degree': 'Electrical, Electronics & Communication '
                                                                            'Engineering',
        },
        {
            'name': 'Jack', 'courses': ['course A', 'course C'], 'degree': 'Education Leadership & Administration',
        },
        {
            'name': 'Mason', 'courses': ['course C', 'course C Hard'], 'degree': 'Business/Commerce',
        },
    ]

    # Set courses info here.
    courses_info = [
        {'code': 'COMPSCI2333', 'name': 'course A', 'prerequisite': [],
         'description': 'course A description', },
        {'code': 'COMPSCI3467', 'name': 'course B', 'prerequisite': [],
         'description': 'course B description', },
        {'code': 'COMPSCI4599', 'name': 'course C', 'prerequisite': ['course B', ],
         'description': 'course C description', },
        {'code': 'COMPSCI4653', 'name': 'course C Hard', 'prerequisite': ['course C', ],
         'description': 'course C Hard description', },
    ]

    # Set events info here.
    events_info = [
        {
            'id': 1,
            'course': 'course A',
            'name': 'event 01',
            'description': 'event 01 description',
            'location': '123.45,234,56',
            'type': Event.lecture,
        },
        {
            'id': 2,
            'course': 'course A',
            'name': 'event 02',
            'description': 'event 02 description',
            'location': '123.45,234,56',
            'type': Event.lab,

        },
        {
            'id': 3,
            'course': 'course B',
            'name': 'event 03',
            'description': 'event 03 description',
            'location': '123.45,234,56',
            'type': Event.tutorial,

        },
        {
            'id': 4,
            'course': 'course B',
            'name': 'event 04',
            'description': 'event 04 description',
            'location': '123.45,234,56',
            'type': Event.lab,

        },
        {
            'id': 5,
            'course': 'course C',
            'name': 'event 05',
            'description': 'event 05 description',
            'location': '123.45,234,56',
            'type': Event.lecture,

        },
        {
            'id': 6,
            'course': 'course C Hard',
            'name': 'event 06',
            'description': 'event 06 description',
            'location': '123.45,234,56',
            'type': Event.lecture,

        },
    ]

    # Set assignments here.
    assignments_info = [
        {'course': 'course A', 'title': 'Assignment 01', 'detail': 'Assignment 01 detail.',
         'deadline': [2022, 3, 21, 12, 0]},
        {'course': 'course A', 'title': 'Assignment 02', 'detail': 'Assignment 02 detail.',
         'deadline': [2022, 3, 22, 12, 0]},
        {'course': 'course B', 'title': 'Assignment 03', 'detail': 'Assignment 03 detail.',
         'deadline': [2022, 3, 21, 9, 0]},
        {'course': 'course C', 'title': 'Assignment 04', 'detail': 'Assignment 04 detail.',
         'deadline': [2022, 4, 1, 12, 0]},
        {'course': 'course C Hard', 'title': 'Assignment 05', 'detail': 'Assignment 05 detail.',
         'deadline': [2022, 4, 1, 18, 0]},
        {'course': 'course C Hard', 'title': 'Assignment 06', 'detail': 'Assignment 06 detail.',
         'deadline': [2022, 4, 2, 19, 0]},
    ]
    # Set grades here.
    grades_info = [
        {'student': 'Jack', 'course': 'course A', 'assignment': 'Assignment 01', 'result': 60, },
        {'student': 'Jack', 'course': 'course A', 'assignment': 'Assignment 02', 'result': 70, },
        {'student': 'Mason', 'course': 'course B', 'assignment': 'Assignment 03', 'result': 80, },
        {'student': 'Amelia', 'course': 'course C', 'assignment': 'Assignment 04', 'result': 90, },
        {'student': 'Amelia', 'course': 'course C Hard', 'assignment': 'Assignment 05', 'result': 100, },
    ]
    # Set degrees here.
    degrees_info = [
        {'name': 'Business Administration and Management', 'courses': ['course A', 'course B', ], },
        {'name': 'Electrical, Electronics & Communication Engineering', 'courses': ['course B', 'course C', ], },
        {'name': 'Education Leadership & Administration', 'courses': ['course A', 'course C', ], },
        {'name': 'Business/Commerce', 'courses': ['course A', 'course B', 'course C', ], },

    ]

    time_slots_info = [
        {'event': 1, 'from': [2022, 1, 10, 12, 30], 'to': [2022, 1, 10, 14, 30]},
        {'event': 2, 'from': [2022, 1, 11, 13, 0], 'to': [2022, 1, 11, 15, 0]},
        {'event': 3, 'from': [2022, 1, 12, 9, 0], 'to': [2022, 1, 12, 11, 0]},
        {'event': 4, 'from': [2022, 1, 13, 11, 30], 'to': [2022, 1, 13, 13, 30]},
        {'event': 5, 'from': [2022, 1, 14, 14, 0], 'to': [2022, 1, 14, 16, 0]},
        {'event': 6, 'from': [2022, 1, 11, 9, 0], 'to': [2022, 1, 11, 11, 30]},
    ]

    populate_user(student_usernames, staff_usernames)
    populate_course(courses_info)
    populate_assignment(assignments_info)
    populate_degree(degrees_info)
    populate_staff(staffs_info)
    populate_student(students_info)
    populate_grade(grades_info)
    populate_event(events_info)
    populate_time_slot(time_slots_info)


if __name__ == '__main__':
    print('Starting LTC++ population script...')
    populate()
    print('Done. Ignore those time zone warnings. Everything is OK.')