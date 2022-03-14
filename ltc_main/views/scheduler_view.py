from xmlrpc.client import FastParser
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.forms.models import ModelMultipleChoiceField
from ..forms import *
from ..models import *
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q
from datetime import date


@login_required
def find_meeting_time(request):
    meetings = TeamMeeting.objects.filter(members=request.user)
    context = {'nbar': "meeting",
               'form': MeetingForm,
               'meetings': meetings, }
    if request.method == 'POST':

        form = MeetingForm(request.POST)
        if form.is_valid():
            # Check that name is unique for this user before save
            #print("This is the meeting id:", form.id)
            meeting = form.save(commit=True)
            meeting.owner.add(User.objects.get(username=request.user))
            meeting.members.add(User.objects.get(username=request.user))
            meeting.saveSlug()
            meeting.save()
            return redirect(reverse('ltc:team_schedule_page',
                                    kwargs={'category_slug':
                                            meeting.slug}))
    return render(request, 'ltc/find_meeting_time.html', context)


@login_required
def team_schedule_page(request, category_slug):

    meeting = get_object_or_404(
        TeamMeeting, slug=category_slug, members=request.user)
    url_parameter = request.GET.get("q")
    fresh = True
    if url_parameter:
        fresh = False
        students = User.objects.filter(Q(username__icontains=url_parameter) | Q(
            first_name__icontains=url_parameter) | Q(last_name__icontains=url_parameter))[:10]
        students = [item for item in students.all(
        ) if item not in meeting.members.all()]
    else:
        students = None
        fresh = True

    context = {'nbar': "meeting",
               'students': students,
               'meeting': meeting,
               'fresh': fresh,
               'slug': category_slug,
               }

    calTimes = [["Monday", []], ["Tuesday", []], [
        "Wedensday", []], ["Thursday", []], ["Friday", []]]
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
        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    return render(request, 'ltc/team_schedule_page.html', context)


def TimeHelper(meeting, calTimes):
    meeting_times = []
    for m in meeting.members.all():
        if m.is_staff:
            u = Staff.objects.filter(user=m).first()
        else:
            u = Student.objects.filter(user=m).first()

        d = str(datetime.date.today().year)+"-W"+str(meeting.weekNumber)
        startDate = datetime.datetime.strptime(d + '-1', "%Y-W%W-%w")
        endDate = datetime.datetime.strptime(d + '-6', "%Y-W%W-%w")
        meeting_times.extend(list(u.timeSlots.all().all_occurrences(
            from_date=startDate, to_date=endDate)))
    for i in range(5):
        calTimes[i][0]=calTimes[i][0] + " ({date})".format(date=(startDate.date()+ datetime.timedelta(days=i)).strftime("%d, %b"))
    t = [1]*7200
    for m in meeting_times:
        a = m[0].weekday()*1440+m[0].hour*60+m[0].minute
        b = m[1].weekday()*1440+m[1].hour*60+m[1].minute
        print(a, b)
        t[a:b] = [0]*(b-a)
    start = False
    sd = 0
    for i in range(7200):
        if t[i] == 1 and start == False:
            start = True
            sd = i
        if t[i] == 0 and start == True:
            start = False
            appendTimes(calTimes, sd, i)
    if start:
        appendTimes(calTimes, sd, 7199)


def appendTimes(calTimes, sd, ed):
    while sd//1440 != ed//1440:
        calTimes[sd//1440][1].append(('{:02d}:{:02d}'.format(*divmod(sd % 1440, 60)),
                                      '{:02d}:{:02d}'.format(*divmod(1439, 60))))
        sd = (1+sd//1440)*1440
    calTimes[sd//1440][1].append(('{:02d}:{:02d}'.format(*divmod(sd % 1440, 60)),
                                  '{:02d}:{:02d}'.format(*divmod(ed % 1440, 60))))
