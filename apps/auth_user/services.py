import random
from datetime import datetime

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.serializers import ValidationError

from apps.auth_user.models import AuthGroup, User
from apps.auth_user.utils import UserUtils
from apps.core.exceptions import BadRequestException, BaseCustomException
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator


class UserService:
    def __init__(self):
        pass

    # --- Business Logic ---
    def change_user_password(cls, user, current_password, new_password):
        cls.__validate_user_password(user, current_password)
        cls.__validate_allow_password({"password": new_password})

        user.set_password(new_password)
        user.save()

    def verify_user(cls, uid, token):
        user = cls.get_user_from_uidb64(uid)
        cls.__validate_uid_token(token, user)

        user.is_verified = True
        user.save()

    def reset_user_password(cls, uidb64, token, new_password):
        user = cls.get_user_from_uidb64(uidb64)

        cls.__validate_allow_password({"password": new_password})
        cls.__validate_uid_token(token, user)

        user.set_password(new_password)
        user.save()

    def get_user_if_login_success(cls, request, email, password):
        user_by_email = User.objects.filter(email=email)

        user = authenticate(
            request,
            email=email,
            password=password,
        )

        cls.__process_validate_user_login(user_by_email, user)
        
        cls.reset_user_login_attempt(user)
        return user

    def reset_user_login_attempt(cls, user):
        UserUtils.reset_user_login_attempt(user)

    # --- Data Processing ---
    def get_user_data(cls, request):
        data = request.data
        cls.__validate_allow_password(data)

        return {
            **data,
            "is_superuser": False,
            "is_verified": False,
            "is_active": True,
            "groups": getattr(cls.get_default_group(), "id", None),
        }

    def get_default_group(cls):
        default_group = AuthGroup.objects.filter(is_default=True).first()
        return default_group

    def get_user_from_uidb64(cls, uidb64):
        try:
            user_id = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=user_id)
            return user
        except Exception as _:
            return None

    def generate_uidb64(cls, user):
        return urlsafe_base64_encode(force_bytes(user.id))

    def generate_token(cls, user):
        return default_token_generator.make_token(user)

    # --- Validate ---
    def __process_validate_user_login(cls, user_by_email, user):
        if user_by_email.filter(punish_datetime__gte=datetime.now()).exists():
            raise BadRequestException(
                "Your account is temporarily locked. Please try again later."
            )

        if not user:
            _user = user_by_email.first()
            if _user:
                UserUtils.update_user_login_attemp(_user)

            raise BaseCustomException(
                "Invalid email or password",
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.is_active:
            raise BadRequestException("Your account is inactive.")

        if not user.is_verified:
            raise BadRequestException(
                "Your account is not verified. Please check your email."
            )

    def __validate_allow_password(cls, data):
        if len(data.get("password", "")) < 6:
            raise ValidationError(
                {"password": "Password must be at least 6 characters long."}
            )
        
    def __validate_uid_token(cls, token, user):
        if not user or not default_token_generator.check_token(user, token):
            raise BadRequestException("Invalid token")

    def __validate_user_password(self, user, current_password):
        if not user.check_password(current_password):
            raise ValidationError(
                {
                    "current_password": "Current password is incorrect",
                }
            )