from django.contrib import admin
from .models import Exam, ExamResponse, Answer


# Register your models here.
admin.site.register(Exam)
admin.site.register(ExamResponse)
admin.site.register(Answer)