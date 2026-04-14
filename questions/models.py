from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.

class Question(models.Model):
    department = models.ForeignKey(
        'core.Department',
        on_delete=models.CASCADE,
        related_name='questions',
    )
    course = models.ForeignKey(
        'core.Course',
        on_delete=models.CASCADE,
        related_name='questions'
    )

    module = models.ForeignKey(
        'core.Module',
        on_delete=models.CASCADE,
        related_name='questions'
    )

    text = models.TextField(blank=True, null=True)
    explanation = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='questions/', null=True, blank=True)

    # for LaTeX / formulas
    formula = models.TextField(blank=True, null=True)
    difficulty = models.CharField(
        max_length=10,
        choices=[('easy','Easy'), ('medium','Medium'), ('hard','Hard')],
        default='medium'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Question {self.id}"




class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices', null=True, blank=True)
    label = models.CharField(max_length=1)  # A, B, C, D
    text = models.TextField()

    image = models.ImageField(upload_to='choices/', null=True, blank=True)
    is_answer = models.BooleanField(default=False)

    # for LaTeX / formulas
    formula = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Choice {self.label} for Question {self.question.id}"