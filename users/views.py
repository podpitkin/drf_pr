from rest_framework.generics import RetrieveUpdateDestroyAPIView
from users.serializers import UserSerializer


class ProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer