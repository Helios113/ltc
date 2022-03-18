from calendar import c
from xmlrpc.client import FastParser
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.forms.models import ModelMultipleChoiceField
from ..forms import *
from ..models import *
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q
from datetime import date
from datetime import datetime
from django.forms import inlineformset_factory

from django.forms import modelformset_factory

# Create your views here.


@login_required
def index(request):
    user = request.user
    # logout admin to avoid bugs.
    if user.is_superuser:
        return user_logout(request)
    clean_meetings(user)
    # get the relevant user based on their status
    # for each user type extract needed info
    if user.is_staff:
        u = Staff.objects.filter(user=user).first()
    else:
        u = Student.objects.filter(user=user).first()

    assignments = u.get_assignments()
    deadlines = [i for i in assignments if i.deadline > datetime.now()]

    print(u.get_time_slots())

    todaysAgenda = [{"time": "{sTime}-{eTime}".format(
        sTime="{hour:02d}:{minute:02d}".format(
            hour=i[0].hour, minute=i[0].minute),
        eTime="{hour:02d}:{minute:02d}".format(
            hour=i[1].hour, minute=i[1].minute),
    ),
        "link": i[2].slug, 'text':"{cName}: {eName}".format(cName=i[2].course.name,
                                                            eName=i[2].name)}
        for i in u.get_time_slots().all_occurrences(from_date=datetime.now(), to_date=date.today())]
    current_courses = [i for i in u.courses.all() if i.endDate > date.today()]
    context = {
        'person': u,
        'courses_taken': current_courses,
        'time': todaysAgenda,
        'assignments': deadlines
    }
    return render(request, 'ltc/index.html', context)


def clean_meetings(user):
    # Delete the out-dated meeting for user
    thisWeek = date.today().isocalendar()[1]
    meetings = TeamMeeting.objects.filter(owner=user)
    for m in meetings:
        if m.weekNumber < thisWeek:
            TeamMeeting.delete(m)


def register(request):
    form = UserForm()
    registered = False
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            t = form.save()
            t.set_password(t.password)
            # Student
            if form.cleaned_data['identity'] == UserForm.STUDENT:
                t.is_staff = False
                t.save()
                degree = form.cleaned_data['degree']
                s = Student.objects.create(user=t)
                s.degree = degree
                s.save()
            # Professor
            elif form.cleaned_data['identity'] == UserForm.PROFESSOR:
                t.is_staff = True
                t.save()
                p = Staff.objects.create(user=t)
                p.type = Staff.PROFESSOR
                p.save()
            # TA
            elif form.cleaned_data['identity'] == UserForm.TEACHING_ASSISTANT:
                t.is_staff = True
                t.save()
                p = Staff.objects.create(user=t)
                p.type = Staff.TEACHING_ASSISTANT
                p.save()
            # Administrator
            elif form.cleaned_data['identity'] == UserForm.ADMINISTRATOR:
                t.is_staff = True
                t.is_superuser = True
                t.save()
                p = Staff.objects.create(user=t)
                p.type = Staff.ADMINISTRATOR
                p.save()
            else:
                raise RuntimeError('Unknown identity.')
            registered = True
            return redirect('ltc:index')
            
        else:
            print(form.errors)
    else:
        pass
    context = {'form': form, 'registered': registered}
    return render(request, 'ltc/register.html', context)


# Base login view


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('ltc:index'))
            else:
                return HttpResponse("Your LTC++ account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'ltc/login.html')


# Base logout form


@ login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('ltc:index'))


@ login_required
def add_course(request):
    if request.user.is_staff is False:
        return redirect(reverse('ltc:courses'))
    form = CourseForm()
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            obj = form.save()
            Staff.objects.filter(user=request.user)[0].courses.add(obj)
            return redirect(reverse('ltc:courses'))

    context = {'form': form}
    return render(request, 'ltc/add_menus/add_course.html', context)


@ login_required
def add_event(request, slug, type):

    a = get_object_or_404(Course, slug=slug)
    if request.method == 'GET':
        type = type[0:-1]
        data = {'course': a, 'type': type}
        form = EventForm()
        context = {'form': form, 'data': data}
        return render(request, 'ltc/add_menus/add_event.html', context)

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.course = a
            obj.type = type
            obj.save()
            return redirect(reverse('ltc:course_page',
                                    kwargs={'slug':
                                            slug}))
        else:
            data = {'course': a, 'type': type}
            context = {'form': form, 'data': data}
            return render(request, 'ltc/add_menus/add_event.html', context)


@ login_required
def add_assignment(request, slug):
    a = get_object_or_404(Course, slug=slug)

    if request.method == 'GET':
        data = {'course': a}
        form = AssignmentForm()
        context = {'form': form, 'data': data}
        return render(request, 'ltc/add_menus/add_assignment.html', context)

    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.course = a
            obj.save()
            return redirect(reverse('ltc:course_page',
                                    kwargs={'slug':
                                            slug}))
        else:
            data = {'course': a}
            context = {'form': form, 'data': data}
            return render(request, 'ltc/add_menus/add_assignment.html', context)


@ login_required
def course_page(request, slug):
    user = request.user
    if user.is_staff:
        u = Staff.objects.get(user=user)
    else:
        u = Student.objects.get(user=user)
    c = get_object_or_404(Course, slug=slug)
    if c in list(u.courses.all()):
        add = False
    else:
        add = True;
    if request.method == 'POST':
        if add:
            u.courses.add(c)
            add = False
        else:
            u.courses.remove(c)
            add = True
    prerequisites = c.prerequisite.all()
    assignments = c.assignment_set.all()
    events = c.event_set.all()
    staff = Staff.objects.filter(courses = c)
    data = [["Lectures", []], ["Tutorials", []], ["Labs", []]]
    data[0][1] = [i for i in events if i.type == 'Lecture']
    data[1][1] = [i for i in events if i.type == 'Tutorial']
    data[2][1] = [i for i in events if i.type == 'Lab']
    
    context = {'course': c, 'prerequisites': prerequisites,
               'assignments': assignments, 'events': data, 'user': user, 'staff':list(staff), 'add':add}
    return render(request, 'ltc/course_page.html', context)


@ login_required
def event_page(request, slug):
    e = get_object_or_404(Event, slug=slug)
    course = e.course
    context = {
        'event': e,
        'course': course,
    }

    return render(request, 'ltc/event_page.html', context)


@login_required
def assignment_page(request, slug):
    a = get_object_or_404(Assignment, slug=slug)
    course = a.course
    title = a.title
    detail = a.detail
    context = {'assignment': a, 'course': course,
               'title': title, 'detail': detail}
    return render(request, 'ltc/assignment_page.html', context)


# Maybe not needed


@login_required
def grade_page(request, slug):
    g = get_object_or_404(Grade, slug=slug)
    student = g.student
    staff = g.staff
    course = g.course

    context = {
        'grade': g,
        'student': student,
        'staff': staff,
        'course': course,
    }
    return render(request, 'ltc/grade_page.html', context)


@login_required
def edit_course(request, slug):
    c = get_object_or_404(Course, slug=slug)
    form = CourseForm(instance=c)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=c)
        if form.is_valid():
            form.save()
            return redirect('ltc:course_page', c.slug)
        else:
            print(form.errors)
    else:
        pass
    context = {'form': form, 'slug': slug}
    return render(request, 'ltc/edit_menus/edit_course.html', context)


@login_required
def edit_assignment(request, slug):
    a = get_object_or_404(Assignment, slug=slug)
    form = AssignmentForm(instance=a)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=a)
        if form.is_valid():
            form.save()
            return redirect('ltc:assignment_page', a.slug)
        else:
            print(form.errors)
    else:
        pass
    context = {'form': form, 'slug': slug}
    return render(request, 'ltc/edit_menus/edit_assignment.html', context)


# Base course view
# Aggregate page for courses


def courses(request):
    user = request.user
    # get the relevant user based on their status
    # for each user type extract needed info
    if user.is_staff:
        u = Staff.objects.filter(user=user).first()
    else:
        u = Student.objects.filter(user=user).first()
    courses = u.courses.all()
    context = {
        'nbar': 'courses',
        'courses': courses
    }
    return render(request, 'ltc/courses.html', context)


def edit_anything(request, model_class, form_class, html, slug, url):
    i = get_object_or_404(model_class, slug=slug)
    form = form_class(instance=i)
    if request.method == 'POST':
        form = form_class(request.POST, instance=i)
        if form.is_valid():
            form.save()
            return redirect(url, i.slug)
    context = {'form': form, 'slug': slug}
    return render(request, html, context)


@login_required
def edit_grade(request, slug):
    return edit_anything(request, Grade, GradeForm, 'ltc/edit_grade.html', slug, 'ltc:grade_page')


# @login_required
# def edit_degree(request, slug):
#     return edit_anything(request, Degree, DegreeForm, 'ltc/edit_degree.html', slug, 'ltc:degree_page')


@login_required
def edit_event(request, slug):
    return edit_anything(request, Event, EventForm, 'ltc/edit_menus/edit_event.html', slug, 'ltc:event_page')


# Find meeting page


@login_required
def grades(request):
    user = request.user
    u = Student.objects.filter(user=user).first()

    # All grades belonging to a student
    allGrades = Grade.objects.filter(student=u)

    # Courses wth grades
    courses = allGrades.values_list('course').distinct()

    courseList = []
    for c in courses:
        grade_query = allGrades.filter(course=c[0])
        courseList.append(
            {"id": c[0], "name": grade_query[0].course, "grades": grade_query})

    context = {"data": courseList,
               "nbar": "grades"}
    return render(request, 'ltc/grades.html', context)


@login_required
def staff_grades(request):
    user = request.user
    u = Staff.objects.filter(user=user).first()

    context = {"data": u.get_assignments(),
               "nbar": "grades"}
    return render(request, 'ltc/staff_grades.html', context)

@login_required
def grade_assignment(request, slug):
    a = get_object_or_404(Assignment, slug=slug)
    # generate a membership form for the given employee
    GradingForm = make_grading_form(a)
    size = Student.objects.filter(courses=a.course).count()
    GradingFormSet = modelformset_factory(
        Grade, form=GradingForm, max_num=size, extra=size)

    if request.method == "POST":
        formset = GradingFormSet(
            request.POST, queryset=Grade.objects.filter(assignment=a))
        if formset.is_valid():
            instances = formset.save(commit=False)
            for member in instances:
                member.assignment = a
                member.course = a.course
                member.save()
            formset.save_m2m()
            return redirect('ltc:staff_grades')
    else:
        formset = GradingFormSet(queryset=Grade.objects.filter(assignment=a),)
    return render(request, 'ltc/grade_assignment.html', {'formset': formset})

@login_required
def join_course(request):
    user = request.user
    if user.is_staff:
        u = Staff.objects.get(user=user)
        courses = Course.objects.all();
    else:
        u = Student.objects.get(user=user)
        courses = u.degree.course.all()
    courses = list(set(courses) - set(u.courses.all()))
    context = {"courses": courses,
               "nbar": "join",
               "u":u}
    return render(request, 'ltc/join_course.html', context)