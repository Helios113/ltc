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


def populate_staff(staffs):
    for info in staffs:
        s = Staff.objects.get_or_create(user=User.objects.get(username=info['name']))[0]
        s.type = info['type']
        s.save()
    return


def populate_student(student_usernames):
    for name in student_usernames:
        t = Student.objects.get_or_create(user=User.objects.get(username=name))[0]
        t.save()
    return


def populate_course(courses):
    for course in courses:
        t = Course.objects.get_or_create(name=course['name'])[0]
        t.code = course['code']
        t.staff = Staff.objects.get_or_create(user=User.objects.get(username=course['staff']))[0]
        t.description = course['description']
        t.prerequisite.set([Course.objects.get(name=pre) for pre in course['prerequisite']])
        t.save()
    return


# def populate_event(events):
#     for info in events:
#         e = Event.objects.get_or_create(course=Course.objects.get(name=info['course']), name=info['name'])[0]
#         e.location = info['location']
#         e.address = info['address']
#         e.student.set([Student.objects.get(user=User.objects.get(username=student)) for student in info['student']])
#         #e.time_slot.set([TimeSlot.objects.get(day=day, time=time) for day, time in info['time_slot']])
#         e.save()
#     return


# def populate_assignment(assignments):
#     for info in assignments:
#         t = Assignment.objects.create(course=Course.objects.get(name=info['course']), title=info['title'])
#         t.detail = info['detail']
#         t.save()
#     return


# def populate_grade(grades):
#     for info in grades:
#         g = Grade.objects.create(student=Student.objects.get(user=User.objects.get(username=info['student'])),
#                                  staff=Staff.objects.get(user=User.objects.get(username=info['staff'])),
#                                  course=Course.objects.get(name=info['course']))
#         g.name = info['name']
#         g.result = info['result']
#         g.save()
#     return


# def populate_degree(degrees):
#     for info in degrees:
#         d = Degree.objects.create(name=info['name'])
#         d.course.set(Course.objects.filter(name__in=info['courses']))
#         d.save()
#     return


def populate():
    # Set usernames here.
    # The default email is username plus '@student.gla.ac.uk'
    # The default password is username plus '123'.
    student_usernames = ['Amelia', 'Emily', 'Jack', 'Mason', ]
    staff_usernames = ['Charlotte', 'Harry', ]
    staffs = [{'name': 'Charlotte', 'type': Staff.PROFESSOR, },
              {'name': 'Harry', 'type': Staff.TEACHING_ASSISTANT, }]

    # Set courses info here.
    courses = [
        {'code': 'COMPSCI2333', 'name': 'course A', 'prerequisite': [], 'description': 'course A description', 'staff': 'Harry', },
        {'code': 'COMPSCI3467', 'name': 'course B', 'prerequisite': [], 'description': 'course B description', 'staff': 'Harry', },
        {'code': 'COMPSCI4599', 'name': 'course C', 'prerequisite': ['course B'], 'description': 'course C description',
         'staff': 'Charlotte', },
        {'code': 'COMPSCI4653', 'name': 'course C Hard', 'prerequisite': ['course A', 'course C'], 'description': 'course C Hard description',
         'staff': 'Charlotte', },
    ]

    # Set events info here.
    events = [
        {
            'course': 'course A',
            'name': 'Lecture',
            'student': ['Amelia', 'Jack', ],
            'location': '123.45,234,56',
            'address': 'The classroom 1001',
            #'time_slot': [(TimeSlot.MON, 9), (TimeSlot.MON, 9.25), (TimeSlot.MON, 9.5), (TimeSlot.MON, 9.75), ]
        },
        {
            'course': 'course A',
            'name': 'Laboratory',
            'student': ['Amelia', 'Jack', ],
            'location': '123.45,234,56',
            'address': 'The classroom 1001',
            #'time_slot': [(TimeSlot.MON, 10), (TimeSlot.MON, 10.25), (TimeSlot.MON, 10.5), (TimeSlot.MON, 10.75), ]
        },
        {
            'course': 'course B',
            'name': 'Lecture',
            'student': ['Amelia', 'Emily', 'Mason', ],
            'location': '123.45,234,56',
            'address': 'The classroom 1001',
            #'time_slot': [(TimeSlot.MON, 10), (TimeSlot.MON, 10.25), (TimeSlot.MON, 10.5), (TimeSlot.MON, 10.75), ]
        },
        {
            'course': 'course B',
            'name': 'Laboratory',
            'student': ['Amelia', 'Emily', 'Mason', ],
            'location': '123.45,234,56',
            'address': 'The classroom 1001',
            #'time_slot': [(TimeSlot.TUE, 10), (TimeSlot.TUE, 10.25), ]
        },
        {
            'course': 'course C',
            'name': 'Lecture',
            'student': ['Amelia', 'Emily', ],
            'location': '123.45,234,56',
            'address': 'The classroom 1001',
            #'time_slot': [(TimeSlot.MON, 11), (TimeSlot.MON, 11.25), (TimeSlot.MON, 11.5), (TimeSlot.MON, 11.75), ]
        },
        {
            'course': 'course C Hard',
            'name': 'Lecture',
            'student': ['Amelia', ],
            'location': '123.45,234,56',
            'address': 'The classroom 1001',
            #'time_slot': [(TimeSlot.MON, 12), (TimeSlot.MON, 12.25), (TimeSlot.MON, 12.5), (TimeSlot.MON, 12.75), ]
        },
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
    # Set grades here.
    grades = [
        {'student': 'Jack', 'staff': 'Harry', 'course': 'course A', 'name': 'AE 03', 'result': 'A4', },
        {'student': 'Jack', 'staff': 'Harry', 'course': 'course A', 'name': 'Final Exam', 'result': 'A2', },
        {'student': 'Mason', 'staff': 'Harry', 'course': 'course B', 'name': 'Final Exam', 'result': 'A5', },
        {'student': 'Amelia', 'staff': 'Charlotte', 'course': 'course C', 'name': 'Paper Reading', 'result': 'B2', },
        {'student': 'Amelia', 'staff': 'Charlotte', 'course': 'course C Hard', 'name': 'Quiz 01', 'result': 'A3', },
    ]
    # Set degrees here.
    degrees = [
        {'name': 'Business Administration and Management', 'courses': ['course A', 'course B', ], },
        {'name': 'Electrical, Electronics & Communication Engineering', 'courses': ['course B', 'course C', ], },
        {'name': 'Education Leadership & Administration', 'courses': ['course A', 'course C', ], },
        {'name': 'Business/Commerce', 'courses': ['course A', 'course B', 'course C', ], },

    ]

    #populate_time_slot()
    populate_user(student_usernames, staff_usernames)
    # The Staff points to the User, so the User goes first.
    populate_staff(staffs)
    # The Student points to the User.
    populate_student(student_usernames)
    # The Course points to the staff.
    # populate_course(courses)
    # The Assignment points to the Course
    #populate_assignment(assignments)
    # The Event points to the Course
    #populate_event(events)
    #populate_grade(grades)
    #populate_degree(degrees)


if __name__ == '__main__':
    print('Starting LTC++ population script...')
    populate()
    print('Done.')
