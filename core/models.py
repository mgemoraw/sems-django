import base64
from django.db import models
from django.utils import timezone
# Create your models here.


class University(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, unique=True)
    slag = models.SlugField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.name



class College(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField()
    university = models.ForeignKey('University', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class School(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='schools')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
            return self.name


class Faculty(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=50, null=True, blank=True)
    slag = models.SlugField()
    college = models.ForeignKey('College', on_delete=models.CASCADE, null=True, blank=True)
    university = models.ForeignKey('University', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)

    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='departments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
    
class Program(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='programs')
    Faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='programs')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    


class Chair(models.Model):
    name = models.CharField(max_length=100, unique=True)
    faculty = models.ForeignKey('Faculty', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Module(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='modules')
    courses = models.ManyToManyField('Course', related_name='modules')
    file = models.FileField(upload_to='module_files/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    code = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    module = models.ForeignKey('Module', on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# class Course(models.Model):
#     module = models.ForeignKey('Module', on_delete=models.SET_NULL, null=True, blank=True)

#     code = models.CharField(max_length=10, unique=True)
#     name = models.CharField(max_length=255)
#     slug = models.SlugField()
#     credit_hour = models.IntegerField()

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


#     # questions = models.ForeignKey('Question', on_delete=models.CASCADE, null=True, related_name='course_questions')

#     def __str__(self):
#         return self.name


# class Module(models.Model):
#     name = models.CharField(max_length=255)
#     department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)
#     # courses = models.ForeignKey('Course', on_delete=models.CASCADE, null=True, related_name='module_courses')

#     def __str__(self):
#         return self.name


    # tests = models.ForeignKey('exams.Exam', on_delete=models.CASCADE,null=True, related_name='department_tests')
    # questions = models.ForeignKey('questions.Question', on_delete=models.CASCADE,null=True, related_name='department_questions')
    # modules = models.ForeignKey('Module', on_delete=models.CASCADE, null=True, related_name='department_modules')

    # def __str__(self):
    #     return self.name