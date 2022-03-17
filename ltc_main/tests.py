from django.test import TestCase
from .models import *
from datetime import datetime


# Create your tests here.

class StaffModelTests(TestCase):

    def test_staff(self):
        """
        Test if the staff has the appropriate permissions
        """
        harry = User(username='Harry')
        harry.set_password('Harry123')
        harry.is_staff = True
        s = Staff(user=harry)
        s.type = Staff.PROFESSOR
        self.assertIs(s.type == Staff.PROFESSOR, True)
        self.assertIs(s.user.is_staff, True)


class StudentModelTests(TestCase):

    def test_time_slots(self):
        """
        Test if the get_time_slots() function works.
        """
        course = Course.objects.create(name='Math')
        event01 = Event.objects.create(course=course, name='event 01')
        event02 = Event.objects.create(course=course, name='event 02')
        time_slot01 = TimeSlot.objects.create(
            event=event01,
            start=datetime(2022, 3, 17, 12, 0),
            end=datetime(2022, 3, 17, 14, 0),
            repeat='RRULE:FREQ=WEEKLY'
        )
        time_slot02 = TimeSlot.objects.create(
            event=event02,
            start=datetime(2022, 3, 16, 14, 0),
            end=datetime(2022, 3, 16, 16, 0),
            repeat='RRULE:FREQ=WEEKLY'
        )
        user = User.objects.create(username='student')
        student = Student.objects.create(user=user)
        student.courses.add(course)
        time_slots = student.get_time_slots()
        self.assertQuerysetEqual(
            time_slots,
            ['<TimeSlot: 2022-03-16 14:00:00>', '<TimeSlot: 2022-03-17 12:00:00>']
        )

    def test_assignments(self):
        """
        Test if the get_assignments() function works.
        """
        course = Course.objects.create(name='Math')
        Assignment.objects.create(course=course,title='quiz')
        Assignment.objects.create(course=course, title='exam')

        user = User.objects.create(username='student')
        student = Student.objects.create(user=user)
        student.courses.add(course)
        assignments = student.get_assignments()
        self.assertQuerysetEqual(
            assignments,
            ['<Assignment:  Math quiz>', '<Assignment:  Math exam>']
        )
