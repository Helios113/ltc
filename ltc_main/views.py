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


def add_course(request):
    form = CourseForm()
    added = False
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            t = form.save()
            added = True
        else:
            print(form.errors)
    else:
        pass
    context = {'form': form, 'added': added}
    return render(request, 'ltc/add_course.html', context)


def add_assignment(request):
    form = AssignmentForm()
    added = False
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            t = form.save()
            added = True
        else:
            print(form.errors)
    else:
        pass
    context = {'form': form, 'added': added}
    return render(request, 'ltc/add_assignment.html', context)


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('ltc:index'))


@login_required
def student_page(request):
    try:
        s = request.user.student
    except:
        error_msg = "You are not a logged student."
        context = {'error_msg': error_msg}
        return render(request, 'ltc/index.html', context)

    courses = s.course_set.all()
    context = {'student': s, 'courses': courses}
    return render(request, 'ltc/student_page.html', context)

@login_required
def professor_page(request):
    try:
        p = request.user.professor
    except:
        error_msg = "You are not a logged professor."
        context = {'error_msg': error_msg}
        return render(request, 'ltc/index.html', context)

    courses = p.course_set.all()
    context = {'professor': p, 'courses': courses}
    return render(request, 'ltc/professor_page.html', context)


def course_page(request, slug):
    try:
        c = Course.objects.get(slug=slug)
    except:
        error_msg = "Course not found."
        context = {'error_msg': error_msg}
        return render(request, 'ltc/index.html', context)
    prerequisite = c.prerequisite.all()
    student = c.student.all()
    time_period = c.time_period.all()
    context = {'course': c, 'prerequisite': prerequisite, 'student': student, 'time_period': time_period, }
    return render(request, 'ltc/course_page.html', context)
