from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Staff)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Assignment)
admin.site.register(Event)
admin.site.register(Grade)
admin.site.register(Degree)
admin.site.register(TeamMeeting)

