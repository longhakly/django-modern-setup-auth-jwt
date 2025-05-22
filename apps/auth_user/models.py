from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    Permission,
)
from django.db import models
from apps.core.models import AbstractModel


class GroupManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, name):
        return self.get(name=name)

    async def aget_by_natural_key(self, name):
        return await self.aget(name=name)
    

class AuthGroup(AbstractModel):
    name = models.CharField(max_length=150, unique=True)
    is_default = models.BooleanField(default=False)
    permissions = models.ManyToManyField(Permission, blank=True)
    objects = GroupManager()

    class Meta:
        db_table = "auth_user_group"

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.save()
        return user
    

class User(AbstractBaseUser, AbstractModel):
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    groups = models.ForeignKey(
        AuthGroup,
        on_delete=models.CASCADE,
        related_name="user_groups",
        blank=True,
        null=True,
    )
    login_attempt = models.IntegerField(default=0)
    punish_datetime = models.DateTimeField(blank=True, null=True)
    objects = UserManager()
    USERNAME_FIELD = "email"

    class Meta:
        db_table = "auth_user_user"

    def __str__(self):
        return self.email

    def user_permissions(self):
        if not self.groups:
            return Permission.objects.none()
        return self.groups.permissions.all()

    def has_perm(self, perm, obj=None):
        user_perms = self.user_permissions()
        return self.is_superuser or (
            user_perms and user_perms.filter(codename=perm).exists()
        )

    def has_module_perms(self, app_label):
        user_perms = self.user_permissions()
        return self.is_superuser or (
            user_perms and user_perms.filter(content_type__app_label=app_label).exists()
        )