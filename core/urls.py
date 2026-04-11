from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ChairViewSet,
    ProgramViewSet,
    UniversityViewSet,
    SchoolViewSet,
    FacultyViewSet,
    DepartmentViewSet,
    CourseViewSet,
    ModuleViewSet,
)

router = DefaultRouter()
router.register(r'universities', UniversityViewSet)
router.register(r'schools', SchoolViewSet)
router.register(r'faculties', FacultyViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'modules', ModuleViewSet)
router.register(r'chairs', ChairViewSet)
router.register(r'programs', ProgramViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
