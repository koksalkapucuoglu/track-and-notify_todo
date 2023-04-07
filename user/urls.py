from django.urls import path

from rest_framework import routers

from user.views import (
    CreateUserView, MeView, UpdateUserApiView, ChangePasswordAPIView,
    ForgotPasswordView, ResetPasswordViewSet
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()

router.register(r'me', MeView, basename='me')
router.register(r'reset_password', ResetPasswordViewSet,
                basename='reset_password')

urlpatterns = [
    path('create_user/', CreateUserView.as_view(), name='create_user'),
    path('get_token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh_token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/', ChangePasswordAPIView.as_view(),
         name='change_password'),
    path('forgot_password/', ForgotPasswordView.as_view(),
         name='forgot_password'),
    path('update_information/<int:pk>/', UpdateUserApiView.as_view(),
         name='update_user'),
] + router.urls