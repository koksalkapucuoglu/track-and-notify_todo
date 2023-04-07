import uuid
from datetime import datetime, timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.generics import (
    CreateAPIView, GenericAPIView, UpdateAPIView
)
from rest_framework.permissions import IsAuthenticated, AllowAny

from core.exceptions import prettier_exc
from core.permissions import IsOwner
from user.serializers import (
    UserSerializer, UserUpdateSerializer, ChangePasswordSerializer,
    ForgotPasswordSerializer, ResetPasswordSerializer
)
from core.exceptions import (
    ResetPasswordTokenHasExpiredException, InvalidResetPasswordTokenException
)
from user.models import ResetPasswordToken

User = get_user_model()


class CreateUserView(CreateAPIView):
    serializer_class = UserSerializer


class MeView(ViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ('get',)

    def list(self, request):
        user_data_dict = {
            "id": str(request.user.id),
            "username": request.user.username,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email,
            "is_superuser": request.user.is_superuser
        }
        return Response(user_data_dict)


class UpdateUserApiView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    http_method_names = ['patch']  # Only allow PATCH method

    def get_object(self):
        obj = get_object_or_404(self.queryset, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj


class ChangePasswordAPIView(GenericAPIView):
    queryset = ''
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def put(self, request):
        data = JSONParser().parse(request)
        serializer = self.serializer_class(
            data=data, context={'request': request})
        if serializer.is_valid():
            return Response(
                {'message': 'Password successfully changed'},
                status=status.HTTP_200_OK)

        if serializer.is_valid():
            return Response(
                {'message': 'Password successfully changed'},
                status=status.HTTP_200_OK)
        return Response(
            prettier_exc(serializer.errors), status=status.HTTP_400_BAD_REQUEST
        )


class ForgotPasswordView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ForgotPasswordSerializer

    def _set_forgot_password_token(self, email):
        user = User.objects.get(email=email)

        token = str(uuid.uuid4())
        reset_password_token = ResetPasswordToken.objects.create(
            user=user,
            token=token,
            expired_at=datetime.now() + timedelta(hours=1)
        )
        reset_password_token.save()

        return token

    def _send_forgot_password_email(self, email):
        token = self._set_forgot_password_token(email)

        url = f'{settings.BASE_URL}/reset_password?token={token}'

        subject = 'Reset your password'
        message = render_to_string('forgot_password_email.html', {'url': url})
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]

        send_mail(
            subject, message, from_email, recipient_list, fail_silently=False
        )

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        self._send_forgot_password_email(email)

        return Response({'success': 'Password reset email sent successfully'})


class ResetPasswordViewSet(GenericViewSet):
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]
    queryset = ResetPasswordToken.objects.none()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        query_params = request.query_params
        token = query_params.get('token') if query_params else None

        try:
            reset_password_token = ResetPasswordToken.objects.get(token=token)

            if datetime.now().astimezone() > reset_password_token.expired_at:
                raise ResetPasswordTokenHasExpiredException()

            # Reset the user's password and delete the reset password token
            user = reset_password_token.user
            user.set_password(serializer.validated_data.get('password'))
            user.save()
            reset_password_token.delete()

            return Response(
                {'message': 'Password reset successful'},
                status=status.HTTP_200_OK
            )

        except ResetPasswordToken.DoesNotExist:
            raise InvalidResetPasswordTokenException()
