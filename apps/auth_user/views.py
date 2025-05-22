from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from apps.auth_user.models import User
from apps.auth_user.serializers import UserSerializer, UserListSerializer
from apps.auth_user.services import UserService
from apps.core.exceptions import BadRequestException, BaseCustomException
from apps.core.services.email_service import EmailService
from apps.core.services.jwt_service import JWTService
from apps.core.views import CoreCreateViewSet, CoreListViewSet


class UserCreateView(CoreCreateViewSet):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        __user_service = UserService()

        data = __user_service.get_user_data(request)
        serializer, instance = self.create_user(data)

        try:
            # TODO: Implement with Celery
            EmailService().send_verify_email(instance)
        except Exception as _:
            pass

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def create_user(self, data):
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        instance = serializer.instance
        instance.set_password(data.get("password"))
        instance.save()
        return serializer, instance


class UserLoginView(CoreCreateViewSet):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        data = request.data
        email = data.get("email")
        password = data.get("password")

        __user_service = UserService()

        user = __user_service.get_user_if_login_success(
            request,
            email,
            password,
        )

        return JWTService().response_login_jwt(user)


class UserLogoutView(CoreCreateViewSet):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refreshToken")

        if refresh_token:
            JWTService().revork_jwt_token(refresh_token)

        return JWTService().response_logout_jwt()


class UserRefeshTokenView(CoreCreateViewSet):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refreshToken")
        if not refresh_token:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        try:
            return JWTService().response_refresh_token_jwt(refresh_token)
        except Exception as _:
            raise BaseCustomException(
                "Invalid refresh token",
                status=status.HTTP_401_UNAUTHORIZED,
            )


class UserVerifyView(CoreListViewSet):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def list(self, request, *args, **kwargs):
        uid, token = kwargs.get("uid"), kwargs.get("token")
        UserService().verify_user(uid, token)
        return Response(status=status.HTTP_200_OK)


class UserSendResetPasswordView(CoreCreateViewSet):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        email = request.data.get("email")

        user = User.objects.filter(email=email).first()
        if not user:
            raise ValidationError(
                {
                    "email": "Invalid email",
                }
            )

        try:
            EmailService().send_reset_email(user)
        except Exception as _:
            pass

        return Response(status=status.HTTP_200_OK)


class UserResetPasswordView(CoreCreateViewSet):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        uid, token = kwargs.get("uid"), kwargs.get("token")
        password = request.data.get("password")
        UserService().reset_user_password(uid, token, password)
        return Response(status=status.HTTP_200_OK)


class UserChangePasswordView(CoreCreateViewSet):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        current_password = request.data.get("current_password")
        password = request.data.get("password")

        UserService().change_user_password(
            user,
            current_password,
            password,
        )

        return Response(status=status.HTTP_200_OK)


class UserCurrentView(CoreListViewSet):
    model = User
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
