from rest_framework import serializers
from .models import ExamResponse, Answer
from questions.models import Question, Choice

# ----------------------------
# Answer Serializer
# ----------------------------
class AnswerSerializer(serializers.ModelSerializer):
    question_text = serializers.ReadOnlyField(source='question.text')
    choice_text = serializers.ReadOnlyField(source='selected_choice.text')

    class Meta:
        model = Answer
        fields = ['id', 'question', 'question_text', 'selected_choice', 'choice_text']

# ----------------------------
# ExamResponse Serializer
# ----------------------------
class ExamResponseSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    user = serializers.ReadOnlyField(source='user.username')
    exam_title = serializers.ReadOnlyField(source='exam.title')

    class Meta:
        model = ExamResponse
        fields = ['id', 'exam', 'exam_title', 'user', 'status', 'score', 'started_at', 'submitted_at', 'answers', 'answers_json']

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        response = ExamResponse.objects.create(**validated_data)

        # Create each Answer
        for ans_data in answers_data:
            Answer.objects.create(response=response, **ans_data)

        return response

    def update(self, instance, validated_data):
        # Allow updating only before submission
        if instance.status == 'submitted':
            raise serializers.ValidationError("Cannot modify submitted response")

        answers_data = validated_data.pop('answers', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if answers_data:
            # Update answers
            for ans_data in answers_data:
                ans_obj, created = Answer.objects.update_or_create(
                    response=instance,
                    question=ans_data['question'],
                    defaults={'selected_choice': ans_data['selected_choice']}
                )
        return instance