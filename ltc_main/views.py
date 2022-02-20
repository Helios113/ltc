from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.forms.models import ModelMultipleChoiceField
from .forms import *
from .models import *


# Create your views here.
def index(request):
    students = Student.objects.all()
    staffs = Staff.objects.all()
    courses = Course.objects.all()
    events = Event.objects.all()
    assignments = Assignment.objects.all()
    time_slots = TimeSlot.objects.all()
    grades = Grade.objects.all()
    degrees = Degree.objects.all()
    context = {
        'students': students,
        'staffs': staffs,
        'courses': courses,
        'events': events,
        'assignments': assignments,
        'time_slots': time_slots,
        'grades': grades,
        'degrees': degrees,
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
                p = Staff.objects.create(user=t)
                p.type = Staff.PROFESSOR
                p.save()
            elif form.cleaned_data['identity'] == UserForm.TEACHING_ASSISTANT:
                t.is_staff = True
                t.save()
                p = Staff.objects.create(user=t)
                p.type = Staff.TEACHING_ASSISTANT
                p.save()
            elif form.cleaned_data['identity'] == UserForm.ADMINISTRATOR:
                t.is_staff = True
                t.is_superuser = True
                t.save()
                p = Staff.objects.create(user=t)
                p.type = Staff.ADMINISTRATOR
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
def add_event(request):
    return add_anything(request, EventForm, 'ltc/add_event.html')


@login_required
def add_assignment(request):
    return add_anything(request, AssignmentForm, 'ltc/add_assignment.html')


@login_required
def add_time_slot(request):
    return add_anything(request, TimeSlotForm, 'ltc/add_time_slot.html')


@login_required
def add_grade(request):
    return add_anything(request, GradeForm, 'ltc/add_grade.html')


@login_required
def add_degree(request):
    return add_anything(request, DegreeForm, 'ltc/add_degree.html')


@login_required
def student_page(request, slug):
    s = get_object_or_404(Student, slug=slug)
    events = s.event_set.all()
    courses = s.get_courses()
    available_time_slots = s.get_available_time_slots()
    context = {'student': s, 'courses': courses, 'events': events, 'available_time_slots': available_time_slots}
    return render(request, 'ltc/student_page.html', context)


@login_required
def staff_page(request, slug):
    p = get_object_or_404(Staff, slug=slug)
    courses = p.course_set.all()
    available_time_slots = p.get_available_time_slots()
    context = {'staff': p, 'courses': courses, 'available_time_slots': available_time_slots}
    return render(request, 'ltc/staff_page.html', context)


@login_required
def course_page(request, slug):
    c = get_object_or_404(Course, slug=slug)
    prerequisites = c.prerequisite.all()
    assignments = c.assignment_set.all()
    events = c.event_set.all()
    context = {'course': c, 'prerequisites': prerequisites,
               'assignments': assignments, 'events': events, }
    return render(request, 'ltc/course_page.html', context)


@login_required
def event_page(request, slug):
    e = get_object_or_404(Event, slug=slug)
    course = e.course
    students = e.student.all()
    time_slots = e.time_slot.all()
    context = {
        'event': e,
        'course': course,
        'students': students,
        'time_slots': time_slots,
    }
    return render(request, 'ltc/event_page.html', context)


@login_required
def assignment_page(request, slug):
    a = get_object_or_404(Assignment, slug=slug)
    course = a.course
    title = a.title
    detail = a.detail
    context = {'assignment': a, 'course': course, 'title': title, 'detail': detail}
    return render(request, 'ltc/assignment_page.html', context)


@login_required
def time_slot_page(request, slug):
    t = get_object_or_404(TimeSlot, slug=slug)
    day = t.day
    time = t.time
    context = {'time_slot': t, 'day': day, 'time': time}
    return render(request, 'ltc/time_slot_page.html', context)


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
def degree_page(request, slug):
    d = get_object_or_404(Degree, slug=slug)
    courses = d.course.all()

    context = {
        'degree': d,
        'courses': courses,
    }
    return render(request, 'ltc/degree_page.html', context)


@login_required
def delete_student(request, slug):
    s = get_object_or_404(Student, slug=slug)
    if s.user == request.user:
        user_logout(request)
    s.delete()
    return redirect('ltc:index')


@login_required
def delete_staff(request, slug):
    p = get_object_or_404(Staff, slug=slug)
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
def delete_event(request, slug):
    e = get_object_or_404(Event, slug=slug)
    e.delete()
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
def delete_grade(request, slug):
    g = get_object_or_404(Grade, slug=slug)
    g.delete()
    return redirect('ltc:index')


@login_required
def delete_degree(request, slug):
    d = get_object_or_404(Degree, slug=slug)
    d.delete()
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
        form = AssignmentForm(request.POST, instance=a)
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


@login_required
def edit_degree(request, slug):
    return edit_anything(request, Degree, DegreeForm, 'ltc/edit_degree.html', slug, 'ltc:degree_page')


@login_required
def edit_event(request, slug):
    return edit_anything(request, Event, EventForm, 'ltc/edit_event.html', slug, 'ltc:event_page')


@login_required
def find_meeting_time(request):
    # students = Student.objects.all()
    time_slots = ''
    form = MeetingForm()
    # form.fields['student'] = ModelMultipleChoiceField(students)
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            time_slots = TimeSlot.objects.all()
            for s in form.cleaned_data['student']:
                time_slots = time_slots & s.get_available_time_slots()
        else:
            print(form.errors)
    else:
        pass
    context = {
        'form': form,
        'time_slots': time_slots,
    }
    return render(request, 'ltc/find_meeting_time.html', context)
