from rest_framework import serializers
from apps.auth_user.models import User, AuthGroup


class AuthGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthGroup
        fields = ["id", "name"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["is_superuser", "password", "created_at", "updated_at", "last_login"]
        extra_kwargs = {
            "is_verified": {"write_only": True},
            "is_active": {"write_only": True},
            "login_attempt": {"write_only": True},
            "punish_datetime": {"write_only": True},
        }


class UserListSerializer(serializers.ModelSerializer):
    groups_info = AuthGroupSerializer(source="groups", many=False)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "groups_info",
        ]
