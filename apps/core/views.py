from rest_framework import viewsets
from rest_framework import generics


class CoreViewSet(viewsets.ModelViewSet):
    filterset_fields = "__all__"
    ordering_fields = "__all__"
    ordering = "-id"


class CoreListViewSet(generics.ListAPIView):
    filterset_fields = "__all__"
    ordering_fields = "__all__"
    ordering = "-id"
    
    
class CoreCreateViewSet(generics.CreateAPIView):
    pass


class CoreRetrieveViewSet(generics.RetrieveAPIView):
    pass


class CoreUpdateViewSet(generics.UpdateAPIView):
    pass

class CoreDeleteViewSet(generics.DestroyAPIView):
    pass