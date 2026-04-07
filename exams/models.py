from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.

def current_year():
    return timezone.now().year


class Exam(models.Model):
    # YEAR_CHOICES = [(y, y) for y in range(2022, 2035)]
    # year = models.IntegerField(choices=YEAR_CHOICES)
    questions = models.ManyToManyField(
        'questions.Question',
        through='ExamQuestion',
        related_name='exams'
    )
    title = models.CharField(max_length=255)
    year = models.IntegerField(default=current_year)

    department = models.ForeignKey('core.Department', on_delete=models.CASCADE, related_name='exams')

    created_by = models.ForeignKey('api.User', on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.year})"
    

class ExamQuestion(models.Model):
    exam = models.ForeignKey('Exam', on_delete=models.CASCADE)
    question = models.ForeignKey('questions.Question', on_delete=models.CASCADE)

    order = models.PositiveIntegerField()
    marks = models.FloatField(default=1)

    def clean(self):
        if self.question.department != self.exam.department:
            raise ValidationError("Question must belong to same department as exam")
        
    # 👇 ADD IT HERE
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('exam', 'question')
        ordering = ['order']


# ----------------------------
# Exam Response
# ----------------------------
class ExamResponse(models.Model):
    exam = models.ForeignKey(
        'Exam',
        on_delete=models.CASCADE,
        related_name='responses'
    )
    user = models.ForeignKey(
        'api.User',
        on_delete=models.CASCADE,
        related_name='exam_responses'
    )

    # Attempt tracking
    status = models.CharField(
        max_length=20,
        choices=[('in_progress', 'In Progress'), ('submitted', 'Submitted')],
        default='in_progress'
    )
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    
    # Total score
    score = models.FloatField(default=0)

    # Optional fast retrieval of answers (JSON)
    answers_json = models.JSONField(null=True, blank=True)

    class Meta:
        unique_together = ('exam', 'user')  # prevent duplicate attempts

    def __str__(self):
        return f"Response by {self.user.username} for {self.exam.title}"

    def submit(self):
        """
        Call this when the student submits the exam
        - calculates score
        - sets status to submitted
        - stores answers JSON for fast retrieval
        """
        # from questions.models import Answer  # avoid circular import
        
        self.status = 'submitted'
        self.submitted_at = timezone.now()

        # Calculate score
        total_score = 0
        answers = self.answers.all()
        answers_data = {}

        for ans in answers:
            answers_data[str(ans.question.id)] = ans.selected_choice.id
            if ans.selected_choice.is_correct:
                total_score += ans.question.marks if hasattr(ans.question, 'marks') else 1

        self.score = total_score
        self.answers_json = answers_data
        self.save()


class Answer(models.Model):
    response = models.ForeignKey(
        ExamResponse,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    question = models.ForeignKey(
        'questions.Question',
        on_delete=models.CASCADE
    )
    selected_choice = models.ForeignKey(
        'questions.Choice',
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('response', 'question')  # only one answer per question

    def clean(self):
        # Ensure the question belongs to the exam
        if self.question not in self.response.exam.questions.all():
            raise ValidationError(
                "This question does not belong to the selected exam"
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.response.user.username} - Q{self.question.id}"
    


class Test(models.Model):
    pass