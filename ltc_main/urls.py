from django.urls import path
from . import views

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

    # Pages for viewing items.
    path('student_page/<slug:slug>/', views.student_page, name='student_page'),
    path('professor_page/<slug:slug>/', views.professor_page, name='professor_page'),
    path('course_page/<slug:slug>/', views.course_page, name='course_page'),
    path('courses', views.courses, name='courses'),
    path('assignment_page/<slug:slug>/', views.assignment_page, name='assignment_page'),
    path('time_slot_page/<slug:slug>/', views.time_slot_page, name='time_slot_page'),

    # Pages for deleting items.
    path('delete_student/<slug:slug>/', views.delete_student, name='delete_student'),
    path('delete_professor/<slug:slug>/', views.delete_professor, name='delete_professor'),
    path('delete_course/<slug:slug>/', views.delete_course, name='delete_course'),
    path('delete_assignment/<slug:slug>/', views.delete_assignment, name='delete_assignment'),
    path('delete_time_slot/<slug:slug>/', views.delete_time_slot, name='delete_time_slot'),


    # Pages for editing items.
    path('edit_course/<slug:slug>/', views.edit_course, name='edit_course'),
    path('edit_assignment/<slug:slug>/', views.edit_assignment, name='edit_assignment'),
    path('edit_time_slot/<slug:slug>/', views.edit_time_slot, name='edit_time_slot'),
]
