from django.contrib import admin
from .models import User, University, Department, Role, RoleAssignment, UserResponse, Question, Chair, Faculty, Choice, Course, CourseAssignment, Test, Module, Mail, College, ModelExam, UserExamResponse
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
class UserAdmin(BaseUserAdmin):
    list_display = (
        'username',
        "first_name",
        "last_name",
        'email',
        'role',
        'user_status',
        'department',
        'is_staff',
        'created_at',
    )

    list_filter = (
        'role',
        'user_status',
        'is_staff',
        'department',
    )

    search_fields = ('username', 'email', 'name')

    ordering = ('username', 'first_name', 'last_name')

    readonly_fields = ('created_at', 'updated_at', 'created_by')

    fieldsets = (
        ('Authentication', {
            'fields': ('username', 'password')
        }),
        ('Personal Info', {
            'fields': ('name', 'email', 'department')
        }),
        ('Roles & Status', {
            'fields': ('role', 'user_status', 'must_change_password')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Tracking', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'role', 'department'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk: # only when creating
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        queryset.update(user_status='active')

    def make_inactive(self, request, queryset):
        queryset.update(user_status='inactive')



class ModelExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'exam_start', 'exam_end', 'created_by', 'hide')
    list_filter = ('created_by', 'department', 'exam_start', 'exam_end')
    search_fields = ['title']

admin.site.register(ModelExam, ModelExamAdmin)
admin.site.register(UserExamResponse)

admin.site.register(User, UserAdmin)
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


