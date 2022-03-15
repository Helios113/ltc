from django.urls import path
from .views import views
from .views import timetable_views
from .views import scheduler_view
app_name = 'ltc'

urlpatterns = [
    # Pages for authentication.
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Pages for adding new items.
    path('add_course/', views.add_course, name='add_course'),
    path('add_assignment/', views.add_assignment, name='add_assignment'),
    path('add_time_slot/', views.add_time_slot, name='add_time_slot'),
    path('add_grade/', views.add_grade, name='add_grade'),
    path('add_degree/', views.add_degree, name='add_degree'),

    # Pages for viewing items.
    path('student_page/<slug:slug>/', views.student_page, name='student_page'),
    path('staff_page/<slug:slug>/', views.staff_page, name='staff_page'),
    path('course_page/<slug:slug>/', views.course_page, name='course_page'),
    path('courses', views.courses, name='courses'),
    path('assignment_page/<slug:slug>/',
         views.assignment_page, name='assignment_page'),
    path('time_slot_page/<slug:slug>/',
         views.time_slot_page, name='time_slot_page'),
    path('grade_page/<slug:slug>/', views.grade_page, name='grade_page'),
    path('degree_page/<slug:slug>/', views.degree_page, name='degree_page'),

    # Pages for deleting items.
    path('delete_student/<slug:slug>/',
         views.delete_student, name='delete_student'),
    path('delete_staff/<slug:slug>/', views.delete_staff, name='delete_staff'),
    path('delete_course/<slug:slug>/', views.delete_course, name='delete_course'),
    path('delete_assignment/<slug:slug>/',
         views.delete_assignment, name='delete_assignment'),
    path('delete_time_slot/<slug:slug>/',
         views.delete_time_slot, name='delete_time_slot'),

    path('delete_grade/<slug:slug>/', views.delete_grade, name='delete_grade'),
    path('delete_degree/<slug:slug>/', views.delete_degree, name='delete_degree'),


    # Pages for editing items.
    path('edit_course/<slug:slug>/', views.edit_course, name='edit_course'),
    path('edit_assignment/<slug:slug>/',
         views.edit_assignment, name='edit_assignment'),
    path('edit_time_slot/<slug:slug>/',
         views.edit_time_slot, name='edit_time_slot'),

    path('edit_grade/<slug:slug>/', views.edit_grade, name='edit_grade'),
    path('edit_degree/<slug:slug>/', views.edit_degree, name='edit_degree'),


    # Event create, edit and delete
    path('add_event/', views.add_event, name='add_event'),
    path('event_page/<slug:slug>/', views.event_page, name='event_page'),
    path('edit_event/<slug:slug>/', views.edit_event, name='edit_event'),
    path('delete_event/<slug:slug>/', views.delete_event, name='delete_event'),

    # Find meeting time
    path('find_meeting_time/', scheduler_view.find_meeting_time,
         name='find_meeting_time'),
    path('find_meeting_time/<slug:category_slug>/team_schedule_page/',
         scheduler_view.team_schedule_page, name='team_schedule_page'),

    # Grades
    path('grade/', views.grades, name='grades'),

    # TimeTable
    path('timetable/time_table/', timetable_views.timetable, name='timetable'),

     path('staff_grades/', views.staff_grades, name='staff_grades'),


]
