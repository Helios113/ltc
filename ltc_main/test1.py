from django.test import TestCase
from .forms import *


class Setup_Class(TestCase):

    def setUp(self):
        

        self.user = User.objects.create(username="Harry", password="Harry123",identity ="Professor")
        self.coursea =Course.objects.create(code="COMPSCI2333",endDate="2022-01-01",name="course A",
        description ="course A description",prerequisite=[],)
        self.assignmenta= User.objects.create(course="coursea",title="Assignment 01",detail="Assignment 01 detail",
       deadline="2022-01-01 00:00:00" )

class User_Form_Test(TestCase):

    # Valid Form Data
    def test_UserForm_valid(self):
        form = UserForm(data={'username': "Harry", 'password': "Harry123",'identity':"Professor"})
        self.assertTrue(form.is_valid())

    # Invalid Form Data
    def test_UserForm_invalid(self):
        form = UserForm(data={'username': "", 'password': "",'identity':""})
        self.assertFalse(form.is_valid())

class Course_Form_Test(TestCase):

    def test_CourseForm_valid(self):
        form = CourseForm(data={'code': "COMPSCI2333", 'name': "course A",'endDate':"2022-01-01", 'prerequisite': [],
         'description': "course A description",})
        self.assertTrue(form.is_valid())

    def test_CourseForm_invalid(self):
        form = CourseForm(data={'code': "", 'name': "",'endDate':"", 'prerequisite': [],
         'description': "",})
        self.assertFalse(form.is_valid())    