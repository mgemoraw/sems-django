from django.contrib.auth.models import User as AuthUser, Group
from rest_framework import generics, renderers
from .serializers import AuthUserSerializer, GroupSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from rest_framework import status, permissions, serializers, viewsets
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db import transaction
from datetime import timedelta
from .models import User, Role, Department, Question
from .serializers import UserSerializer, RoleSerializer, UserCreateSerializer, UserLoginSerializer, RoleCreateSerializer, PasswordCreateSerializer, QuestionSerializer
from .authentication import create_access_token, authenticate_user
from rest_framework.authtoken.models import Token 

from drf_yasg.utils import swagger_auto_schema

# Create your views here.


class AuthUserViewSet(viewsets.ModelViewSet):
    queryset = AuthUser.objects.all().order_by('-date_joined')
    serializer_class = AuthUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    # @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class GroupsViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class QuestionsViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by('id')
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]



@swagger_auto_schema(
    method='post',
    request_body=UserLoginSerializer,  # Specify the serializer for the request body
    responses={200: 'Login successful!', 400: 'Invalid credentials'}
)
@api_view(['POST'])
def signup_view(request):
    data = {}
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])

        token=Token.objects.create(user=user)

        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def token_view(request):
    data = {}
    return Response(data=data)

# Create your views here.
class UserLoginViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    @action(detail=True, methods=['post'])
    def login(self, request, pk=None):
        user = self.get_object()
        return Response({'status': 'User logged in'})
    

@api_view(['POST'])
def login_view(request):

    serializer = UserLoginSerializer(data=request.data)

    if serializer.is_valid():
        username = serializer.validated_data['usrename']
        password = serializer.validated_data['password']
        
        # authenticate user
        user = authenticate_user(username, password)

        if not user:
            return JsonResponse({'detail': "Invalid credentials"}, status=400)
        
        # Prepare data to encode in the JWT token
        user_data = {"sub": user.username, "user_id": user.id}

        # Create an access token
        access_token = create_access_token(user_data, expires_delta=timedelta(minutes=120))

        # Return the access token in the response
        return JsonResponse({"access_token": access_token, "token_type": "bearer"})
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# Greet View
class GreetView(APIView):
    def get(self, request):
        return Response({"Greet": "Greetings "}, status=status.HTTP_200_OK)

    def post(self, request):
        return Response({"data": None})


# User Registration View
class UserRegisterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        user_data = UserCreateSerializer(data=data)
        if user_data.is_valid():
            user = User.objects.filter(username=user_data.validated_data['username']).first()
            if user:
                return Response({"detail": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

            department = Department.objects.filter(name=user_data.validated_data['department']).first()
            if not department:
                return Response({"detail": "Department not found"}, status=status.HTTP_404_NOT_FOUND)

            # Hash the password using Django's make_password() function
            password_hash = make_password(user_data.validated_data['password'])
             # Create a new user with the hashed password
            user = User(
                username=user_data.validated_data['username'],
                email=user_data.validated_data['email'],
                password=password_hash,  # Store the hashed password
                role=user_data.validated_data['role'],
                department=department
            )
            user.save()  # Save the user to the database

           
            return Response({"detail": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(user_data.errors, status=status.HTTP_400_BAD_REQUEST)


# User Update View
class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        user = get_object_or_404(User, id=id)
        user_data = UserCreateSerializer(user, data=request.data, partial=True)
        if user_data.is_valid():
            user_data.save()
            return Response({"detail": "Update Successful"}, status=status.HTTP_200_OK)
        return Response(user_data.errors, status=status.HTTP_400_BAD_REQUEST)


# User Delete View
class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        user = get_object_or_404(User, id=id)
        user.delete()
        return Response({"detail": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# Password Update View
class PasswordUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        password_data = PasswordCreateSerializer(data=request.data)
        if password_data.is_valid():
            current_user = request.user
            if not current_user.check_password(password_data.validated_data['old_password']):
                return Response({"detail": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

            current_user.set_password(password_data.validated_data['new_password'])
            current_user.save()
            return Response({"detail": "Password updated successfully"}, status=status.HTTP_200_OK)
        return Response(password_data.errors, status=status.HTTP_400_BAD_REQUEST)


# Token Authentication View
class TokenView(APIView):
    def post(self, request):
        user_data = UserLoginSerializer(data=request.data)
        if user_data.is_valid():
            user = authenticate_user(user_data.validated_data['username'], user_data.validated_data['password'])
            if user:
                access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(hours=1))
                department = user.department.name
                return Response({
                    "access_token": access_token,
                    "token_type": "bearer",
                    "username": user.username,
                    "role": user.role,
                    "department": department,
                }, status=status.HTTP_200_OK)
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(user_data.errors, status=status.HTTP_400_BAD_REQUEST)


# User Logout View
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response({"detail": "Logout Successful"})
        response.delete_cookie('access_token')
        return response


# User List View
class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    

# Role List View
class RoleListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)


# Create Role View
class RoleCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        role_data = RoleCreateSerializer(data=request.data)
        if role_data.is_valid():
            role_data.save()
            return Response(role_data.data, status=status.HTTP_201_CREATED)
        return Response(role_data.errors, status=status.HTTP_400_BAD_REQUEST)


# Assign User Role View
class AssignUserRoleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        new_role = request.data.get("role")
        user = get_object_or_404(User, id=user_id)
        user.role = new_role
        user.save()
        return Response({"detail": "Role assigned successfully"}, status=status.HTTP_200_OK)
