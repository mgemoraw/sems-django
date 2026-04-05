from django.db import models

# Create your models here.

class University(models.Model):
    name = models.CharField(max_length=255)


class School(models.Model):
    name = models.CharField(max_length=255)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='schools')


class Faculty(models.Model):
    name = models.CharField(max_length=255)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='faculties')


class Department(models.Model):
    name = models.CharField(max_length=255)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='departments')


class Course(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')


class Module(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='modules')
    courses = models.ManyToManyField(Course, related_name='modules')
    file = models.FileField(upload_to='module_files/', null=True, blank=True)
