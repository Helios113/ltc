from django.urls import path
from ltc_main import views
app_name = 'ltc'

urlpatterns = [
    path('', views.index, name='index')
]