from xmlrpc.client import FastParser
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.forms.models import ModelMultipleChoiceField
from .forms import *
from .models import *
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q
from datetime import date

# Create your views here.
@login_required
def index(request):
    user = User.objects.filter(username = request.user).first()
    
    # get the relevant user based on their status
    # for each user type extract needed info
    if user.is_staff:
        u = Staff.objects.filter(user= user).first()
        deadlines=""
    else:
        u = Student.objects.filter(user= user).first()
        assignments = u.assignment.all() # check if this is true
        deadlines = [list(i.deadline.all_occurrences(from_date=date.today())) for i in assignments]
    
    # u.timeSlots
    
    context = {
        'person': u,
        'courses_taken': u.courses.all(),
        'time': u.timeSlots.all_occurrences(from_date=date.today()),
        'assignments' : deadlines
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
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('ltc:index'))

# Add base view
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


# Student page view
# TODO: make it use the not simple template
@login_required
def student_page(request, slug):
    s = get_object_or_404(Student, slug=slug)
    events = s.event_set.all()
    courses = s.get_courses()
    available_time_slots = s.get_available_time_slots()
    context = {'student': s, 'courses': courses, 'events': events, 'available_time_slots': available_time_slots}
    return render(request, 'ltc/student_page.html', context)

# Staff page view
@login_required
def staff_page(request, slug):
    p = get_object_or_404(Staff, slug=slug)
    courses = p.course_set.all()
    available_time_slots = p.get_available_time_slots()
    context = {'staff': p, 'courses': courses, 'available_time_slots': available_time_slots}
    return render(request, 'ltc/staff_page.html', context)

# Course page view
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

# Maybe not needed
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

# Base course view
# Aggregate page for courses
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

# Find meeting page
@login_required
def find_meeting_time(request):
    meetings = TeamMeeting.objects.filter(members=request.user)
    context={   'nbar' : "meeting",
                'form' : MeetingForm,
                'meetings': meetings,}
    if request.method == 'POST':
        
        form = MeetingForm(request.POST)
        if form.is_valid():
            #Check that name is unique for this user before save
            #print("This is the meeting id:", form.id)
            meeting = form.save(commit=True)
            meeting.members.add(User.objects.get(username=request.user))
            meeting.saveSlug()
            meeting.save()
            return redirect(reverse('ltc:team_schedule_page',
                                        kwargs={'category_slug':
                                                meeting.slug}))
    return render(request, 'ltc/find_meeting_time.html', context)

@login_required
def team_schedule_page(request, category_slug):

    meeting = get_object_or_404(TeamMeeting, slug=category_slug, members = request.user)
    url_parameter = request.GET.get("q")
    fresh = True
    if url_parameter:
        fresh = False
        students = User.objects.filter(Q(username__icontains=url_parameter) | Q(first_name__icontains=url_parameter) | Q(last_name__icontains=url_parameter) )[:10]
        students = [item for item in students.all() if item not in meeting.members.all()]
    else:
        students = None
        fresh = True

    context = { 'nbar' : "meeting",
                'students': students,
                'meeting': meeting,
                'fresh': fresh,
                'slug':category_slug,
    }
    
    calTimes = [["Monday",[]], ["Tuesday",[]], ["Wedensday",[]], ["Thursday",[]], ["Friday",[]]]
    TimeHelper(meeting, calTimes)
    context['times'] = calTimes
    

    if request.method == 'POST':
        print(request.POST['user'])
        meeting.members.add(User.objects.get(username=request.POST['user']))
    if request.is_ajax():        
        html = render_to_string(
            template_name="ltc/student_search_partial.html", 
            context={'students': students}
        )
        print(html)
        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    
    return render(request, 'ltc/team_schedule_page.html',context)

def TimeHelper(meeting, calTimes):
    meeting_times = []
    for m in meeting.members.all():
        if m.is_staff:
            u = Staff.objects.filter(user = m).first()
        else:
            u = Student.objects.filter(user = m).first()

        d = str(datetime.date.today().year)+"-W"+str(meeting.weekNumber)
        startDate = datetime.datetime.strptime(d + '-1', "%Y-W%W-%w")
        endDate = datetime.datetime.strptime(d + '-6', "%Y-W%W-%w")
        print("DATE: ", startDate,endDate)
        meeting_times.extend(list(u.timeSlots.all().all_occurrences(from_date =startDate,to_date=endDate)))
    t = [1]*7200
    print("Meeting Times", meeting_times)
    for m in meeting_times:
        a = m[0].weekday()*1440+m[0].hour*60+m[0].minute
        b = m[1].weekday()*1440+m[1].hour*60+m[1].minute
        print(a,b)
        t[a:b] = [0]*(b-a)
    start = False
    sd = 0
    for i in range(7200):
        if t[i] == 1 and start == False:
            start = True
            sd = i
        if t[i] == 0 and start == True:
            start = False
            appendTimes(calTimes,sd,i)
    if start:
        appendTimes(calTimes,sd,7199)
    

def appendTimes(calTimes, sd,ed):
    while sd//1440 != ed//1440:
        calTimes[sd//1440][1].append(('{:02d}:{:02d}'.format(*divmod(sd%1440, 60)),
                                   '{:02d}:{:02d}'.format(*divmod(1439, 60))))
        sd = (1+sd//1440)*1440
    calTimes[sd//1440][1].append(('{:02d}:{:02d}'.format(*divmod(sd%1440, 60)),
                                '{:02d}:{:02d}'.format(*divmod(ed%1440, 60))))    
