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
def timetable(request):
    user = request.user
    if user.is_staff:
        u = Staff.objects.filter(user=user).first()
    else:
        u = Student.objects.filter(user=user).first()
        
    if request.is_ajax():
        thisWeek = int(request.GET.get('week', None))
        direction = int(request.GET.get('direction', None))
        weekData = render_to_string(
            template_name="ltc/timetable/time_table_content.html",
            context=timetable_helper(u,thisWeek,direction=direction)
        )
        timeData = render_to_string(
            template_name="ltc/timetable/time_table_data.html",
            context=timetable_helper(u,thisWeek)
        )
        data_dict = {"html_week": weekData,
                     "html_data": timeData}
        return JsonResponse(data=data_dict, safe=False)



    # This week logic based on whatever
    elif request.method == 'GET':
        thisWeek = datetime.date.today().isocalendar()[1]
        return render(request, 'ltc/timetable/time_table.html', timetable_helper(u, thisWeek))

def timetable_helper(u,week,direction=0):
    d = str(datetime.date.today().year)+"-W"+str(week)
    startDate = datetime.datetime.strptime(d + '-1', "%Y-W%W-%w")
    endDate = datetime.datetime.strptime(d + '-6', "%Y-W%W-%w")
    allEventsThisWeek = u.get_time_slots().all_occurrences(from_date=startDate, to_date=endDate)
    
    calTimes = [["Monday", []], ["Tuesday", []], [
        "Wedensday", []], ["Thursday", []], ["Friday", []]]
    for i in range(5):
        calTimes[i][0]=calTimes[i][0] + " ({date})".format(date=(startDate.date()+ datetime.timedelta(days=i)).strftime("%d, %b"))


    for event in allEventsThisWeek:
        data = {"text" : "{:02d}:{:02d} - {:02d}:{:02d}".format(event[0].hour, event[0].minute, event[1].hour,event[1].minute),
        "event":event[2].event }
        calTimes[event[0].day-startDate.day][1].append(data)
    # HOW TO HANDLE EVENTS WHICH SPAN MULTIPLE DAYS
    context={"nbar" : "timetable",
            "week" : week,
            "data":calTimes,
            "direction":direction}
    return context