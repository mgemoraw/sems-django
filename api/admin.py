from django.contrib import admin
from .models import User, University, Department, Role, RoleAssignment, UserResponse, Question, Chair, Faculty, Choice, Course, CourseAssignment, Test, Module, Mail, College, ModelExam, UserExamResponse


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display=('username', 'email', 'role') 

class ModelExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'exam_start', 'exam_end', 'created_by', 'hide')
    list_filter = ('created_by', 'department', 'exam_start', 'exam_end')
    search_fields = ['title']

admin.site.register(ModelExam, ModelExamAdmin)
admin.site.register(UserExamResponse)

admin.site.register(User)
admin.site.register(Role)
admin.site.register(RoleAssignment)

admin.site.register(University)
admin.site.register(Department)
admin.site.register(College)
admin.site.register(Faculty)
admin.site.register(Course)
admin.site.register(Module)

admin.site.register(UserResponse)
admin.site.register(Question)
admin.site.register(Chair)
admin.site.register(Choice)
admin.site.register(Test)
admin.site.register(Mail)


