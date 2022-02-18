from django.urls import path
from . import views

app_name = 'ltc'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('add_course/', views.add_course, name='add_course'),
    path('add_assignment/', views.add_assignment, name='add_assignment'),
    path('logout/', views.user_logout, name='logout'),
    path('student_page/', views.student_page, name='student_page'),
    path('professor_page/', views.professor_page, name='professor_page'),
    path('course_page/<slug:slug>/', views.course_page, name='course_page'),
]
