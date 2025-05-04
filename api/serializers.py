import base64
from rest_framework import serializers
from django.contrib.auth.models import User as AuthUser, Group

from .models import ModelExam, User, Role, University, Department, Chair, Faculty, Choice, Course, Module, Question, Test, UserResponse, Mail, CourseAssignment, RoleAssignment



class AuthUserSerializer(serializers.HyperlinkedModelSerializer):
    groups = serializers.HyperlinkedRelatedField(
        view_name='group-detail', 
        queryset=Group.objects.all(), 
        many=True,
    )
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups', 'password']
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
        fields = ['url', 'name']

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'password', 'role', 'department']

#     def create(self, validated_data):
#         user = User.objects.create_user(**validated_data)
#         return user

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
        fields = ['id', 'name', 'faculty', 'created_at', 'updated_at']


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['id', 'name', 'code', 'college', 'university', 'created_at', 'updated_at']


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'question', 'label', 'content', 'is_answer', 'image_base64']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'module_name', 'module', 'code', 'name', 'credit_hour']


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'name', 'department', 'courses']


class QuestionSerializer(serializers.ModelSerializer):
    options = serializers.JSONField()
    image_base64 = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'department', 'course', 'content', 'options', 'image_base64', 'answer', 'created_at', 'updated_at']
    def get_image_base64(self, obj):
        if obj.image:
            return base64.b64encode(obj.image).decode('utf-8')
        return None


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


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, write_only=True, style={'input_type': 'password'})


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'password',  'department']


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