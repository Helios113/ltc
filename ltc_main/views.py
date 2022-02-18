from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *


# Create your views here.
def index(request):
    context = {}
    if request.user.is_authenticated:
        if request.user.is_staff:
            context = {'professor': Professor.objects.get(user=request.user)}
        else:
            context = {'student': Student.objects.get(user=request.user)}
    return render(request, 'ltc/index.html', context)


def register(request):
    form = UserForm()
    registered = False
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            t = form.save()
            t.set_password(t.password)
            if form.cleaned_data['identity'] == UserForm.STUDENT:
                t.is_staff = False
                t.save()
                s = Student.objects.create(user=t)
                s.save()
            elif form.cleaned_data['identity'] == UserForm.PROFESSOR:
                t.is_staff = True
                t.save()
                p = Professor.objects.create(user=t)
                p.save()
            else:
                raise RuntimeError('Unknown identity. Ask Xinyu for help.')
            registered = True
        else:
            print(form.errors)
    else:
        pass
    context = {'form': form, 'registered': registered}
    return render(request, 'ltc/register.html', context)


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


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('ltc:index'))


def add_anything(request, Form, html):
    form = Form()
    added = False
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            t = form.save()
            added = True
        else:
            print(form.errors)
    else:
        pass
    context = {'form': form, 'added': added}
    return render(request, html, context)


@login_required
def add_course(request):
    return add_anything(request, CourseForm, 'ltc/add_course.html')


@login_required
def add_assignment(request):
    return add_anything(request, AssignmentForm, 'ltc/add_assignment.html')


@login_required
def add_time_slot(request):
    return add_anything(request, TimeSlotForm, 'ltc/add_time_slot.html')


@login_required
def student_page(request, slug):
    try:
        s = Student.objects.get(slug=slug)
    except:
        error_msg = "Student not found."
        context = {'error_msg': error_msg}
        return render(request, 'ltc/index.html', context)

    courses = s.course_set.all()
    context = {'student': s, 'courses': courses}
    return render(request, 'ltc/student_page.html', context)


@login_required
def professor_page(request, slug):
    try:
        p = Professor.objects.get(slug=slug)
    except:
        error_msg = "Professor not found."
        context = {'error_msg': error_msg}
        return render(request, 'ltc/index.html', context)

    courses = p.course_set.all()
    context = {'professor': p, 'courses': courses}
    return render(request, 'ltc/professor_page.html', context)


@login_required
def course_page(request, slug):
    try:
        c = Course.objects.get(slug=slug)
    except:
        error_msg = "Course not found."
        context = {'error_msg': error_msg}
        return render(request, 'ltc/index.html', context)
    prerequisites = c.prerequisite.all()
    students = c.student.all()
    time_slots = c.time_slot.all()
    assignments = c.assignment_set.all()
    context = {'course': c, 'prerequisites': prerequisites, 'students': students, 'time_slots': time_slots, 'assignments': assignments, }
    return render(request, 'ltc/course_page.html', context)
    # return render(request, 'ltc/show_everything_page.html', {'everything': context})


@login_required
def time_slot_page(request, slug):
    try:
        t = TimeSlot.objects.get(slug=slug)
    except:
        error_msg = "Time slot not found."
        context = {'error_msg': error_msg}
        return render(request, 'ltc/index.html', context)

    day = t.day
    time = t.time
    context = {'day': day, 'time': time}
    return render(request, 'ltc/time_slot_page.html', context)


@login_required
def assignment_page(request, slug):
    try:
        t = Assignment.objects.get(slug=slug)
    except:
        error_msg = "Assignment not found."
        context = {'error_msg': error_msg}
        return render(request, 'ltc/index.html', context)
    course = t.course
    title = t.title
    detail = t.detail
    context = {'course': course, 'title': title, 'detail': detail}
    return render(request, 'ltc/assignment_page.html', context)
