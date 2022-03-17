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
    return redirect('ltc:courses')


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
def delete_grade(request, slug):
    g = get_object_or_404(Grade, slug=slug)
    g.delete()
    return redirect('ltc:index')


@login_required
def delete_degree(request, slug):
    d = get_object_or_404(Degree, slug=slug)
    d.delete()
    return redirect('ltc:index')
