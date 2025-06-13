from django.contrib.auth.models import User
from rest_framework import generics, permissions
from inventory.serializers.user import UserCreateSerializer
from inventory.permissions import IsSuperUser 



class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperUser]


