from rest_framework.routers import DefaultRouter
from .views import ExamResponseViewSet

router = DefaultRouter()
router.register(r'exam-responses', ExamResponseViewSet, basename='exam-response')

urlpatterns = router.urls