from django.shortcuts import render
from rest_framework import viewsets
from .models import Chair, Program, University, School, Faculty, Department, Course, Module
from .serializers import (
    ChairSerializer,
    ProgramSerializer,
    UniversitySerializer,
    SchoolSerializer,
    FacultySerializer,
    DepartmentSerializer,
    CourseSerializer,
    ModuleSerializer
)

# Create your views here.

class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer


class ChairViewSet(viewsets.ModelViewSet):
    queryset = Chair.objects.all()
    serializer_class = ChairSerializer
    

class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    