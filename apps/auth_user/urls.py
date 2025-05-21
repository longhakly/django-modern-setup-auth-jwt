from django.urls import path, include
from rest_framework import routers

router = routers.SimpleRouter(trailing_slash=False)


urlpatterns = [
    path("", include(router.urls)),
]

