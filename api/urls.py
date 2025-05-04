
from django.urls import path, re_path, include
from rest_framework import routers
# from .views import get_user, create_user
from .views import (CouresViewSet, DepartmentsViewSet, GreetView, UserRegisterView, UserUpdateView, UserDeleteView, PasswordUpdateView, TokenView, UserLogoutView, UserListView, RoleListView, RoleCreateView, AssignUserRoleView,
login_view, signup_view, token_view, AuthUserViewSet, GroupsViewSet, UserViewSet, QuestionsViewSet, TestsViewSet, ModelExamViewSet
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'v1/auth', AuthUserViewSet, basename='v1-auth')
router.register(r'v1/groups', GroupsViewSet, basename='v1-group')
router.register(r'v1/departments', DepartmentsViewSet, basename='v1-department')
router.register(r'v1/questions', QuestionsViewSet, basename='v1-questions')
router.register(r'v1/tests', TestsViewSet, basename='v1-test')
router.register(r'v1/roles', CouresViewSet, basename='v1-role')
router.register(r'v1/courses', CouresViewSet, basename='v1-course')
router.register(r'v1/exams', ModelExamViewSet, basename='v1-exam')





urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path('login', login_view, name='user_login'),
    re_path('signup/', signup_view, name='user_signup'),
    re_path('token/', token_view, name='access_token'),
    # path('auth/login/', login_view, name='user_login'),
    path('auth/users/register/', UserRegisterView.as_view(), name='user_register'),
    # path('auth/users/update/<int:id>/', UserUpdateView.as_view(), name='user_update'),
    # path('auth/users/delete/<int:id>/', UserDeleteView.as_view(), name='user_delete'),
    # path('auth/password/update/', PasswordUpdateView.as_view(), name='password_update'),
    # path('auth/token/', TokenView.as_view(), name='token_auth'),
    # path('auth/users/logout/', UserLogoutView.as_view(), name='user_logout'),
    # path('auth/users/index/', UserListView.as_view(), name='user_list'),
    # path('auth/roles/index/', RoleListView.as_view(), name='role_list'),
    # path('auth/roles/create/', RoleCreateView.as_view(), name='role_create'),
    # path('auth/users/role/assign/<int:user_id>/', AssignUserRoleView.as_view(), name='assign_user_role'),
]


# urlpatterns += router.urls # path('', include(router.urls)),
