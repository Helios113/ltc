from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *


# Create your views here.
def index(request):
    students = Student.objects.all()
    professors = Professor.objects.all()
    courses = Course.objects.all()
    assignments = Assignment.objects.all()
    time_slots = TimeSlot.objects.all()
    context = {
        'students': students,
        'professors': professors,
        'courses': courses,
        'assignments': assignments,
        'time_slots': time_slots,
    }
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
                raise RuntimeError('Unknown identity. Ask Xinyu for detail.')
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


def add_anything(request, form_class, html):
    form = form_class()
    added = False
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
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
    s = get_object_or_404(Student, slug=slug)
    courses = s.course_set.all()
    context = {'student': s, 'courses': courses}
    return render(request, 'ltc/student_page.html', context)


@login_required
def professor_page(request, slug):
    p = get_object_or_404(Professor, slug=slug)
    courses = p.course_set.all()
    context = {'professor': p, 'courses': courses}
    return render(request, 'ltc/professor_page.html', context)


@login_required
def course_page(request, slug):
    c = get_object_or_404(Course, slug=slug)
    prerequisites = c.prerequisite.all()
    students = c.student.all()
    time_slots = c.time_slot.all()
    assignments = c.assignment_set.all()
    context = {'course': c, 'prerequisites': prerequisites, 'students': students, 'time_slots': time_slots,
               'assignments': assignments, }
    return render(request, 'ltc/course_page.html', context)


@login_required
def time_slot_page(request, slug):
    t = get_object_or_404(TimeSlot, slug=slug)
    day = t.day
    time = t.time
    context = {'time_slot': t, 'day': day, 'time': time}
    return render(request, 'ltc/time_slot_page.html', context)


@login_required
def assignment_page(request, slug):
    a = get_object_or_404(Assignment, slug=slug)
    course = a.course
    title = a.title
    detail = a.detail
    context = {'assignment': a, 'course': course, 'title': title, 'detail': detail}
    return render(request, 'ltc/assignment_page.html', context)


@login_required
def delete_student(request, slug):
    s = get_object_or_404(Student, slug=slug)
    if s.user == request.user:
        user_logout(request)
    s.delete()
    return redirect('ltc:index')


@login_required
def delete_professor(request, slug):
    p = get_object_or_404(Professor, slug=slug)
    if p.user == request.user:
        user_logout(request)
    p.delete()
    return redirect('ltc:index')


@login_required
def delete_course(request, slug):
    c = get_object_or_404(Course, slug=slug)
    c.delete()
    return redirect('ltc:index')


@login_required
def delete_assignment(request, slug):
    a = get_object_or_404(Assignment, slug=slug)
    a.delete()
    return redirect('ltc:index')


@login_required
def delete_time_slot(request, slug):
    t = get_object_or_404(TimeSlot, slug=slug)
    t.delete()
    return redirect('ltc:index')


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
    return render(request, 'ltc/edit_course.html', context)


@login_required
def edit_assignment(request, slug):
    a = get_object_or_404(Assignment, slug=slug)
    form = AssignmentForm(instance=a)
    if request.method == 'POST':
        form = Assignment(request.POST, instance=a)
        if form.is_valid():
            form.save()
            return redirect('ltc:assignment_page', a.slug)
        else:
            print(form.errors)
    else:
        pass
    context = {'form': form, 'slug': slug}
    return render(request, 'ltc/edit_assignment.html', context)


@login_required
def edit_time_slot(request, slug):
    t = get_object_or_404(TimeSlot, slug=slug)
    form = TimeSlotForm(instance=t)
    if request.method == 'POST':
        form = TimeSlotForm(request.POST, instance=t)
        if form.is_valid():
            form.save()
            return redirect('ltc:time_slot_page', t.slug)
        else:
            print(form.errors)
    else:
        pass
    context = {'form': form, 'slug': slug}
    return render(request, 'ltc/edit_time_slot.html', context)


def courses(request):
    courses = Course.objects.all()
    context = {
        'nbar' : 'courses',
        'courses': courses
    }
    return render(request, 'ltc/courses.html', context)