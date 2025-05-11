import base64
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
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
    password = models.CharField(max_length=255, default='User#123')
    role = models.CharField(max_length=20, choices=USER_ROLES, default='student')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    department_name=models.CharField(max_length=100, null=True, blank=True)
    
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, related_name='users')
    faculty = models.ForeignKey('Faculty', on_delete=models.SET_NULL, null=True, blank=True)

    tests = models.ForeignKey('Test', null=True, blank=True, on_delete=models.SET_NULL, related_name='user_tests')
    emails = models.ForeignKey('Mail', null=True,blank=True, on_delete=models.SET_NULL, related_name='user_emails')

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
    
    
    def __str__(self):
        return self.name

class Department(models.Model):
    faculty = models.ForeignKey('Faculty', on_delete=models.CASCADE, null=True, related_name='department_faculty')
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    

    tests = models.ForeignKey('Test', on_delete=models.CASCADE,null=True, related_name='department_tests')
    questions = models.ForeignKey('Question', on_delete=models.CASCADE,null=True, related_name='department_questions')
    modules = models.ForeignKey('Module', on_delete=models.CASCADE, null=True, related_name='department_modules')

    def __str__(self):
        return self.name

class College(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField()
    university = models.ForeignKey('University', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
    

class Chair(models.Model):
    name = models.CharField(max_length=100, unique=True)
    faculty = models.ForeignKey('Faculty', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Faculty(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, null=True, blank=True)
    college = models.ForeignKey('College', on_delete=models.CASCADE, null=True, blank=True)
    university = models.ForeignKey('University', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Choice(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE, null=True, related_name='choices')
    label = models.CharField(max_length=10)
    content = models.TextField()
    is_answer = models.BooleanField(default=False)
    image = models.BinaryField(null=True, blank=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    # module_name = models.CharField(max_length=255)
    module = models.ForeignKey('Module', on_delete=models.SET_NULL, null=True, blank=True)
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    credit_hour = models.IntegerField()

    # questions = models.ForeignKey('Question', on_delete=models.CASCADE, null=True, related_name='course_questions')

    def __str__(self):
        return self.name


class Module(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)
    # courses = models.ForeignKey('Course', on_delete=models.CASCADE, null=True, related_name='module_courses')

    def __str__(self):
        return self.name


class Question(models.Model):
    department = models.ForeignKey('Department', on_delete=models.CASCADE, null=True, related_name='department')
    course = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True, blank=True)
    module = models.ForeignKey('Module', on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    options = models.JSONField()  # Store as JSON array
    image = models.BinaryField(null=True, blank=True)
    answer = models.CharField(max_length=10)
    exam_year = models.PositiveIntegerField(null=True, blank=True)
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

    def __str__(self):
        return f"{self.id} - {self.content}"


class ModelExam(models.Model):
    title = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Many to Many relationship to questions
    questions = models.ManyToManyField(Question, blank=True)

    # Exam timings
    duration_minutes = models.PositiveIntegerField(help_text="Duration of the exam in minutes.")
    exam_start = models.DateTimeField(null=True, blank=True)
    exam_end = models.DateTimeField(null=True, blank=True)

    hide = models.BooleanField(default=False)  # Whether the exam is hidden from students

    # Tracking the exam status
    started_at = models.DateTimeField(null=True, blank=True)  # When the student starts the exam
    completed_at = models.DateTimeField(null=True, blank=True)  # When the student completes the exam

    # ForeignKey to responses from students, relation to a student's answers
    user_responses = models.ManyToManyField('UserExamResponse', blank=True)

    def __str__(self):
        return self.title

    def is_active(self):
        """ Check if the exam is within the allowed start/end time range """
        return self.exam_start <= timezone.now() <= self.exam_end

    def start_exam(self, user):
        """ Start the exam for the user, and set the `started_at` field. """
        self.started_at = timezone.now()
        self.save()

        # Create a UserResponse for this user if needed
        if not self.user_responses.filter(user=user).exists():
            response = UserResponse.objects.create(user=user, exam=self)
            self.user_responses.add(response)
            self.save()

    def end_exam(self, user):
        """ End the exam for the user, save the completion time. """
        self.completed_at = timezone.now()
        self.save()

        # You could save the responses here if needed
        user_response = self.user_responses.filter(user=user).first()
        if user_response:
            user_response.save_responses()


class UserExamResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(ModelExam, on_delete=models.CASCADE)
    responses = models.JSONField(default=dict, blank=True)  # Store the responses as a JSON object

    def save_responses(self):
        """ Save or update responses for the user when they submit the exam. """
        # Implement logic to save each question's response (e.g., selected answers)
        pass

    def __str__(self):
        return f"{self.user} - {self.exam.title}"

class Test(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True)
    department = models.ForeignKey('Department', null=True, on_delete=models.CASCADE)
    score = models.FloatField()
    total_questions = models.IntegerField()
    correct_answers = models.IntegerField()
    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)

    responses = models.ForeignKey('UserResponse',null=True, on_delete=models.CASCADE, related_name='test_responses')

    def __str__(self):
        return f"[{self.id}] - {self.score}"


class UserResponse(models.Model):
    test = models.ForeignKey('Test', on_delete=models.CASCADE, null=True,related_name='user_responses')
    question = models.ForeignKey('Question', null=True, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=10)
    is_correct = models.BooleanField()

    def __str__(self):
        return f"[{self.question}] - {self.is_correct}"


class Mail(models.Model):
    user = models.ForeignKey('User', null=True,on_delete=models.CASCADE)
    sender = models.CharField(max_length=255)
    receiver = models.CharField(max_length=255)
    send_at = models.DateTimeField(default=timezone.now)
    received_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.id


class CourseAssignment(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, null=True, blank=True)


class RoleAssignment(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True)
    role = models.ForeignKey('Role', on_delete=models.CASCADE, null=True, blank=True)

