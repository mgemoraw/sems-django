from django.contrib import admin
from.models import (
    University, 
    College,
    School,
    Department, 
    Program, 
    Course, 
    Chair, 
    Faculty,
    )


#Register your models here.
admin.site.register(University)
admin.site.register(Department)
admin.site.register(Program)
admin.site.register(Course)
admin.site.register(Chair)
admin.site.register(Faculty)
admin.site.register(College)
admin.site.register(School)