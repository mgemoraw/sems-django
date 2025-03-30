import base64
from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone


class User(models.Model):
    USER_ROLES = [
        ('user', 'USER'),
        ('student', 'STUDENT'),
        ('admin', 'ADMIN'),
        ('chair', 'CHAIR'),
        ('dean', 'DEAN'),
        ('hoq', 'HOQ'),
        ('hoc', 'HOC'),
    ]

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password_hash = models.CharField(max_length=255, default='User#123')
    role = models.CharField(max_length=20, choices=USER_ROLES, default='student')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    department_name=models.CharField(max_length=100, default=None)
    
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, related_name='users')

    tests = models.ForeignKey('Test', null=True, on_delete=models.CASCADE, related_name='user_tests')
    emails = models.ForeignKey('Mail', null=True, on_delete=models.CASCADE, related_name='user_emails')

    def __str__(self):
        return self.username



class Role(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name


class University(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, unique=True)
    address = models.TextField()
    media_address = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    tests = models.ForeignKey('Test', on_delete=models.CASCADE, related_name='department_tests')
    questions = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='department_questions')
    modules = models.ForeignKey('Module', on_delete=models.CASCADE, related_name='department_modules')


class Chair(models.Model):
    name = models.CharField(max_length=100, unique=True)
    faculty = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class Faculty(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, null=True, blank=True)
    college = models.CharField(max_length=255, null=True, blank=True)
    university = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class Choice(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='choices')
    label = models.CharField(max_length=10)
    content = models.TextField()
    is_answer = models.BooleanField(default=False)


class Course(models.Model):
    module_name = models.CharField(max_length=255)
    module = models.ForeignKey('Module', on_delete=models.SET_NULL, null=True, blank=True)
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    credit_hour = models.IntegerField()

    questions = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='course_questions')


class Module(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)
    courses = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='module_courses')


class Question(models.Model):
    department = models.ForeignKey('Department', on_delete=models.CASCADE, related_name='department')
    course = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    options = models.JSONField()  # Store as JSON array
    image = models.BinaryField(null=True, blank=True)
    answer = models.CharField(max_length=10)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        image_base64 = None
        if self.image:
            image_base64 = base64.b64encode(self.image).decode('utf-8')  # Convert bytes to base64 string

        return {
            'id': self.id,
            'department_id': self.department.id,
            'content': self.content,
            'options': self.options,  # Options are already in JSON format
            'course_idfk': self.course.id if self.course else None,
            'answer': self.answer,
            'image': image_base64,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at),
        }


class Test(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    score = models.FloatField()
    total_questions = models.IntegerField()
    correct_answers = models.IntegerField()
    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)

    responses = models.ForeignKey('UserResponse', on_delete=models.CASCADE, related_name='test_responses')


class UserResponse(models.Model):
    test = models.ForeignKey('Test', on_delete=models.CASCADE, related_name='user_responses')
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=10)
    is_correct = models.BooleanField()


class Mail(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    sender = models.CharField(max_length=255)
    receiver = models.CharField(max_length=255)
    send_at = models.DateTimeField(default=timezone.now)
    received_at = models.DateTimeField(default=timezone.now)


class CourseAssignment(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, null=True, blank=True)


class RoleAssignment(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True)
    role = models.ForeignKey('Role', on_delete=models.CASCADE, null=True, blank=True)

