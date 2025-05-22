from django.urls import path, include
from rest_framework import routers
from apps.auth_user.views import (
    UserCreateView,
    UserLoginView,
    UserLogoutView,
    UserRefeshTokenView,
    UserVerifyView,
    UserSendResetPasswordView,
    UserResetPasswordView,
    UserChangePasswordView,
    UserCurrentView,
)

router = routers.SimpleRouter(trailing_slash=False)


urlpatterns = [
    path("", include(router.urls)),
    path("register", UserCreateView.as_view()),
    path("login", UserLoginView.as_view()),
    path("logout", UserLogoutView.as_view()),
    path("refresh-token", UserRefeshTokenView.as_view()),
    path("verify/<str:uid>/<str:token>", UserVerifyView.as_view()),
    path("send-reset-password", UserSendResetPasswordView.as_view()),
    path("reset-password/<str:uid>/<str:token>", UserResetPasswordView.as_view()),
    path("change-password", UserChangePasswordView.as_view()),
    path("current_user", UserCurrentView.as_view()),
]

