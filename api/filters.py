import django_filters
from .models import Question

class QuestionFilter(django_filters.FilterSet):
    department = django_filters.CharFilter(field_name='department__name', lookup_expr='icontains')
    exam_year = django_filters.NumberFilter(field_name='exam_year')

    class Meta:
        model = Question
        fields = ['department', 'exam_year']
