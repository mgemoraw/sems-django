
from django.urls import path, re_path, include
from rest_framework import routers
# from .views import get_user, create_user
from .views import GreetView, UserRegisterView, UserUpdateView, UserDeleteView, PasswordUpdateView, TokenView, UserLogoutView, UserListView, RoleListView, RoleCreateView, AssignUserRoleView
from .views import login_view, signup_view, token_view, AuthUserViewSet, GroupsViewSet, UserViewSet, QuestionsViewSet


router = routers.DefaultRouter()
router.register(r'users', AuthUserViewSet)
router.register(r'groups', GroupsViewSet)
router.register(r'others', UserViewSet, basename='others')
router.register(r'questions', QuestionsViewSet, basename='questions')



urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),

    re_path('login', login_view, name='user_login'),
    re_path('signup/', signup_view, name='user_signup'),
    re_path('token/', token_view, name='access_token'),
    path('auth/login/', login_view, name='user_login'),
    path('auth/users/register/', UserRegisterView.as_view(), name='user_register'),
    path('auth/users/update/<int:id>/', UserUpdateView.as_view(), name='user_update'),
    path('auth/users/delete/<int:id>/', UserDeleteView.as_view(), name='user_delete'),
    path('auth/password/update/', PasswordUpdateView.as_view(), name='password_update'),
    path('auth/token/', TokenView.as_view(), name='token_auth'),
    path('auth/users/logout/', UserLogoutView.as_view(), name='user_logout'),
    path('auth/users/index/', UserListView.as_view(), name='user_list'),
    path('auth/roles/index/', RoleListView.as_view(), name='role_list'),
    path('auth/roles/create/', RoleCreateView.as_view(), name='role_create'),
    path('auth/users/role/assign/<int:user_id>/', AssignUserRoleView.as_view(), name='assign_user_role'),
]