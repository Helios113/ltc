# This file is to populate some dummy data into the database for testing.
# To do so, run the following command:

# python populate_ltc.py
# python manage.py runserver

# Then, go to http://127.0.0.1:8000/admin/
# To gain administrative access, please log in with the following information.

#   Username: admin
#   Password: 123456

from datetime import datetime
from ltc_main.models import *
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'ltc.settings')


django.setup()


def populate_user(student_usernames, staff_usernames):
    # Set up superuser account.
    admin = User.objects.get_or_create(username='admin')[0]
    admin.set_password('123456')
    admin.email = "admin@student.gla.ac.uk"
    admin.is_staff = True
    admin.is_superuser = True
    admin.save()

    for name in student_usernames:
        f_name = name.split(" ")[0]
        s_name = name.split(" ")[1]
        t = User.objects.get_or_create(username=f_name)[0]
        t.first_name = f_name
        t.second_name = s_name
        # The default email is user's name plus '@student.gla.ac.uk'
        t.email = name + '@student.gla.ac.uk'
        # Students are not staffs
        t.is_staff = False
        # The default password is user's name plus '123'.
        t.set_password(name + '123')
        t.save()

    for name in staff_usernames:
        f_name = name.split(" ")[0]
        s_name = name.split(" ")[1]
        s = User.objects.get_or_create(username=f_name)[0]
        s.first_name = f_name
        s.second_name = s_name
        s.email = name + '@gla.ac.uk'
        s.is_staff = True
        s.set_password(name + '123')
        s.save()
    return


def populate_staff(staffs_info):
    for info in staffs_info:
        s = Staff.objects.get_or_create(
            user=User.objects.get(username=info['name']))[0]
        s.courses.set(Course.objects.filter(name__in=info['courses']))
        s.type = info['type']
        s.save()
    return


def populate_student(students_info):
    for info in students_info:
        t = Student.objects.get_or_create(
            user=User.objects.get(username=info['name']))[0]
        t.courses.set(Course.objects.filter(name__in=info['courses']))
        t.degree = Degree.objects.get(name=info['degree'])
        t.save()
    return


def populate_course(courses_info):
    for info in courses_info:
        t = Course.objects.get_or_create(code=info['code'])[0]
        t.name = info['name']
        t.description = info['description']
        t.prerequisite.set(Course.objects.filter(
            name__in=info['prerequisite']))
        t.save()
    return


def populate_assignment(assignments_info):
    for info in assignments_info:
        t = Assignment.objects.get_or_create(course=Course.objects.get(
            name=info['course']), title=info['title'])[0]
        t.detail = info['detail']
        t.deadline = datetime(*info['deadline'])
        t.save()
    return


def populate_grade(grades_info):
    for info in grades_info:
        g = Grade.objects.get_or_create(student=Student.objects.get(user=User.objects.get(username=info['student'])),
                                        course=Course.objects.get(
                                            name=info['course']),
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
    student_usernames = ['Mikayla Wilkerson',
                         'Nur Ferry', 'Donald Odom', 'Sue Perry', ]
    staff_usernames = ['Radhika Merritt ', 'Peyton Vega', ]

    staffs_info = [{'name': 'Charlotte', 'type': Staff.PROFESSOR, 'courses': ['course A', 'course B']},
                   {'name': 'Harry', 'type': Staff.TEACHING_ASSISTANT, 'courses': ['course C', 'course C Hard']}]
    students_info = [
        {
            'name': 'Mikayla', 'courses': ['Introduction to CS', 'Intermediate CS', 'Database Theory', 'Big Data'],
            'degree': 'Business Administration and Management',
        },
        {
            'name': 'Nur', 'courses': ['Introduction to CS', 'Database Theory'], 'degree': 'Electrical, Electronics & Communication '
                                                                            'Engineering',
        },
        {
            'name': 'Donald', 'courses': ['Intermediate CS', 'Big Data'], 'degree': 'Education Leadership & Administration',
        },
        {
            'name': 'Sue', 'courses': ['Intermediate CS', 'Database Theory'], 'degree': 'Business/Commerce',
        },
    ]

    # Set courses info here.

    courses_info = [
        {'code': 'CS50', 'name': 'Introduction to CS', 'prerequisite': [],
         'description': 'This is an introductory course to computer science taken by all first year students.', },
        {'code': 'CS60', 'name': 'Intermediate CS', 'prerequisite': [],
         'description': 'This is an intermediate course in computer science taken by all first year students.', },
        {'code': 'CS55', 'name': 'Database Theory', 'prerequisite': ['course B', ],
         'description': 'This course covers the basics of databases and the theory behind them. The course also includes practical work.', },
        {'code': 'CS100', 'name': 'Big Data', 'prerequisite': ['course C', ],
         'description': 'The Big Data course covers the basics of Big Data and introduces students to python and fundamental libraries to do Big Data analysis.', },
    ]

    # Set events info here.
    events_info = [
        {
            'course': 'Introduction to CS',
            'name': 'Lecture',
            'description': 'This is the daily CS50 lecture. During these classes we will cover all the basics of CS.',
            'location': 'B1024',
            'geoUri': 'geo:55.87351,-4.29332?z=19',
            'type': Event.lecture,
        },
        {
            'course': 'Introduction to CS',
            'name': 'Lab',
            'description': 'This is the weekly CS50 lab where we do a practical exercise each week.',
            'location': 'James Watt South Room 354',
            'geoUri': 'geo:55.87088,-4.28712?z=19',
            'type': Event.lab,
        },
        {
            'course': 'Introduction to CS',
            'name': 'Tutorial',
            'description': 'This is the monday CS50 Tutorial.',
            'location': 'Hunter Hall East',
            'geoUri': 'geo:55.87121,-4.28832?z=19',
            'type': Event.tutorial,
        },

        {
            'course': 'Intermediate CS',
            'name': 'Lecture',
            'description': 'This is the Tuesday CS60 lecture. During these classes we will cover more advanced topics in CS.',
            'location': 'B1024',
            'geoUri': 'geo:55.87351,-4.29332?z=19',
            'type': Event.lecture,
        },
        {
            'course': 'Intermediate CS',
            'name': 'Lab',
            'description': 'This is the weekly CS60 lab where we do a practical exercise each week.',
            'location': 'James Watt South Room 354',
            'geoUri': 'geo:55.87088,-4.28712?z=19',
            'type': Event.lab,
        },
        {
            'course': 'Intermediate CS',
            'name': 'Tutorial',
            'description': 'This is the Wed CS60 Tutorial.',
            'location': 'Hunter Hall East',
            'geoUri': 'geo:55.87121,-4.28832?z=19',
            'type': Event.tutorial,
        },

        {
            'course': 'Database Theory',
            'name': 'Lecture',
            'description': 'This is the Thursday CS55 lecture. During these classes we will cover more advanced topics in CS.',
            'location': 'B1024',
            'geoUri': 'geo:55.87351,-4.29332?z=19',
            'type': Event.lecture,
        },
        {
            'course': 'Database Theory',
            'name': 'Lab',
            'description': 'This is the weekly CS55 lab where we do a practical exercise each week.',
            'location': 'James Watt South Room 354',
            'geoUri': 'geo:55.87088,-4.28712?z=19',
            'type': Event.lab,
        },
        {
            'course': 'Database Theory',
            'name': 'Tutorial',
            'description': 'This is the Friday CS55 Tutorial.',
            'location': 'Thomson Building 234',
            'geoUri': 'geo:55.87146,-4.28709?z=19',
            'type': Event.tutorial,
        },

        {
            'course': 'Big Data',
            'name': 'Lecture',
            'description': 'This is the Wednesday CS100 lecture. During these classes we will cover more advanced topics in CS.',
            'location': 'B1024',
            'geoUri': 'geo:55.87351,-4.29332?z=19',
            'type': Event.lecture,
        },
        {
            'course': 'Big Data',
            'name': 'Lab',
            'description': 'This is the weekly CS100 lab where we do a practical exercise each week.',
            'location': 'James Watt South Room 354',
            'geoUri': 'geo:55.87088,-4.28712?z=19',
            'type': Event.lab,
        },
        {
            'course': 'Big Data',
            'name': 'Tutorial',
            'description': 'This is the Monday CS100 Tutorial.',
            'location': 'Thomson Building 234',
            'geoUri': 'geo:55.87146,-4.28709?z=19',
            'type': Event.tutorial,
        },
    ]

    # Set assignments here.
    assignments_info = [
        {'course': 'Database Theory', 'title': 'Assignment AE1', 'detail': 'Do some cool Database thing and submit it before the deadline',
         'deadline': [2022, 6, 2, 19, 0]},
        {'course': 'Database Theory', 'title': 'Assignment AE2', 'detail': 'Do some cool Database thing again and submit it before the deadline',
         'deadline': [2022, 8, 2, 19, 0]},
        {'course': 'Intermediate CS', 'title': 'Assignment AE1', 'detail': 'Do some cool CS thing and submit it before the deadline',
         'deadline': [2022, 6, 2, 19, 0]},
        {'course': 'Intermediate CS', 'title': 'Assignment AE2', 'detail': 'Do some cool CS thing again and submit it before the deadline',
         'deadline': [2022, 6, 2, 19, 0]},
        {'course': 'Big Data', 'title': 'Assignment AE1', 'detail': 'Do some cool Big Data thing and submit it before the deadline',
         'deadline': [2022, 6, 2, 19, 0]},
    ]
    # Set grades here.
    grades_info = [
        {'student': 'Mikayla', 'course': 'Database Theory',
            'assignment': 'Assignment AE1', 'result': 60, },
        {'student': 'Mikayla', 'course': 'Database Theory',
            'assignment': 'Assignment AE2', 'result': 90, },

        {'student': 'Donald', 'course': 'Intermediate CS',
            'assignment': 'Assignment AE1', 'result': 70, },
    ]
    # Set degrees here.
    degrees_info = [
        {'name': 'Computer Science',
            'courses': ['Introduction to CS', 'Intermediate CS', 'Database Theory', 'Big Data'], },
    ]

    time_slots_info = [
        {'event': 1, 'from': [2022, 1, 10, 12, 30],
            'to': [2022, 1, 10, 14, 30]},
        {'event': 2, 'from': [2022, 1, 11, 13, 0], 'to': [2022, 1, 11, 15, 0]},
        {'event': 3, 'from': [2022, 1, 12, 9, 0], 'to': [2022, 1, 12, 11, 0]},
        {'event': 4, 'from': [2022, 1, 13, 11, 30],
            'to': [2022, 1, 13, 13, 30]},
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
    print('Done. Everything is OK.')
