from django.contrib import admin
from .models import User, University, Department, Role, RoleAssignment, UserResponse, Question, Chair, Faculty, Choice, Course, CourseAssignment




class UserAdmin(admin.ModelAdmin):
    list_display=('username', 'email', 'role') 

# Register your models here.
admin.site.register(User)
admin.site.register(Role)
admin.site.register(RoleAssignment)

admin.site.register(University)
admin.site.register(Department)
admin.site.register(Faculty)
admin.site.register(Course)

admin.site.register(UserResponse)
admin.site.register(Question)
admin.site.register(Chair)
admin.site.register(Choice)
