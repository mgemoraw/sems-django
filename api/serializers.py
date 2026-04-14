import base64
from rest_framework import serializers
from django.contrib.auth.models import User as AuthUser, Group

from rest_framework import permissions
from .models import ModelExam, User, Role, University, Department, Chair, Faculty, Choice, Course, Module, Question, Test, UserResponse, Mail, CourseAssignment, RoleAssignment
from django.db import transaction

# SErializer classes

class AuthUserSerializer(serializers.HyperlinkedModelSerializer):
    groups = serializers.HyperlinkedRelatedField(
        view_name='group-detail', 
        queryset=Group.objects.all(), 
        many=True,
    )
    class Meta:
        model = User
        # fields = ['url', 'username', 'email', 'groups']
        fields = "__all__"
        extra_kwargs = {'password': {'write_only':True}}
        
    
    def create(self, validated_data):
        groups_data = validated_data.pop('groups', [])
        user = User.objects.create_user(**validated_data)

        # Assign groups after user is created
        user.groups.set(groups_data)
        
        return user
    

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = "__all__"
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'department']

        # exclude = ['groups', 'user_permissions', 'is_superuser', 'is_staff', 'is_active', 'last_login', 'date_joined']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        groups_data = validated_data.pop('groups', [])
        user = User.objects.create_user(**validated_data)
        user = User(**validated_data)

        fname = validated_data.get('first_name', 'user')
        lname = validated_data.get('last_name', 'default')
        default_password = f"{lname}#{fname}123"

        user.set_password(default_password)
        user.must_change_password = True
        user.save()
        user.groups.set(groups_data)

        return user 

    # ---- validation method for username ----
    def validate(self, attrs):
        # if User.objects.filter(username=attrs.get('username')).exists():
        #     raise serializers.ValidationError({"username": "This username is already taken."})
        # if User.objects.filter(email=attrs.get('email')).exists():
        #     raise serializers.ValidationError({"email": "This email is already registered."})
        # return attrs
        username = attrs.get('username')
        email = attrs.get('email')

        queryset = User.objects.all()

        # EXCLUDE current instance during update
        if self.instance:
            queryset = queryset.exclude(id=self.instance.id)

        if username and queryset.filter(username=username).exists():
            raise serializers.ValidationError({"username": "This username is already taken."})

        if email and queryset.filter(email=email).exists():
            raise serializers.ValidationError({"email": "This email is already registered."})

        return attrs
        
    

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description']


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ['id', 'code', 'name', 'address', 'media_address', 'created_at', 'updated_at']


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']


class ChairSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chair
        fields = "__all__"


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['id', 'name', 'code', 'college', 'university', 'created_at', 'updated_at']


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'question', 'label', 'content', 'is_answer', 'image']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'module', 'code', 'name', 'credit_hour']


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'name', 'department', 'courses']


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'label', 'content', 'is_answer', 'image']


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, required=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = [
            'id',
            'department',
            'module',
            'course',
            'content',
            'choices',
            'answer',
            'exam_year',
            'image',
            'image_url',
            'created_at',
            'updated_at',
        ]

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

    def validate(self, data):
        choices = data.get('choices', [])
        answer = data.get('answer')

        if len(choices) < 2:
            raise serializers.ValidationError("At least 2 choices required.")

        labels = [c['label'] for c in choices]

        if answer not in labels:
            raise serializers.ValidationError(
                "Answer must match one of the choice labels."
            )

        if not any(c.get('is_answer') for c in choices):
            raise serializers.ValidationError(
                "At least one choice must be marked as correct."
            )

        return data
    
    def create(self, validated_data):
        choices_data = validated_data.pop('choices')

        with transaction.atomic():
            question = Question.objects.create(**validated_data)

            Choice.objects.bulk_create([
                Choice(question=question, **c)
                for c in choices_data
            ])

        return question

class BulkQuestionSerializer(serializers.Serializer):
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    questions = QuestionSerializer(many=True)

    def create(self, validated_data):
        questions_data = validated_data['questions']
        department = validated_data['department']
        created_questions = []

        with transaction.atomic():
            for q in questions_data:
                q['department'] = department.id  # Set department for each question
                serializer = QuestionSerializer(data=q, context=self.context)
                serializer.is_valid(raise_exception=True)
                created_questions.append(serializer.save())

        return created_questions

class QuestionUploadSerializer(serializers.Serializer):
    # department = serializers.ChoiceField(
    #     choices=[(dept.id, dept.name) for dept in Department.objects.all()],
    #     label="Select Department"
    # )
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all()
        )
    json_file = serializers.FileField()



class BulkOptionSerializer(serializers.Serializer):
    label = serializers.CharField(max_length=10)
    content = serializers.CharField()
    is_answer = serializers.BooleanField(required=False, default=False)

class OptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'question', 'label', 'content', 'is_answer', 'image']
        


class ExamYearQuerySerializer(serializers.Serializer):
    exam_year = serializers.CharField(required=True) 

class ExamDepartmentQuerySerializer(serializers.Serializer):
    department = serializers.CharField(required=True) 


class ExamDepartmentYearQuerySerializer(serializers.Serializer):
    department = serializers.CharField(required=True) 
    exam_year = serializers.CharField(required=True) 


class ExamModuleDepartmentQuerySerializer(serializers.Serializer):
    department = serializers.CharField(required=True) 
    module = serializers.CharField(required=True) 


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id', 'user', 'department', 'score', 'total_questions', 'correct_answers', 'started_at', 'completed_at']


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserResponse
        fields = ['id', 'test', 'question', 'selected_option', 'is_correct']


class MailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mail
        fields = ['id', 'user', 'sender', 'receiver', 'send_at', 'received_at']


class CourseAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseAssignment
        fields = ['id', 'user', 'course']

class RoleAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleAssignment
        fields = ['id', 'user', 'role']

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'department']


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, write_only=True, style={'input_type': 'password'})


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'faculty', 'email', 'role', 'department']


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description']


class RoleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['name', 'description']


class PasswordCreateSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()


class TokenSerializer(serializers.ModelSerializer):
    access_token = serializers.CharField()
    token_type = serializers.CharField()
    username = serializers.CharField()
    role = serializers.CharField()
    department = serializers.CharField()


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, write_only=True, style={'input_type': 'password'})


class ModelExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelExam
        fields = ('title', 'department', 'exam_start', 'exam_end', 'duration_minutes', 'hide')

        # Optional: mark read-only fields
        read_only_fields = ('created_by', 'created_at')

    def create(self, validated_data):
        # Assign the created_by field using the context (viewset handles this)
        user = self.context['request'].user
        exam = ModelExam.objects.create(created_by=user, **validated_data)
        return exam