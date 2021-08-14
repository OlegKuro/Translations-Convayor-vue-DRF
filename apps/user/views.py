from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_200_OK
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, logout
import base64

from user.serializers import MeSerializer


class LoginView(CreateAPIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        user = authenticate(**request.data)
        if user is not None:
            password = request.data['password']
            email = user.email
            return Response({
                'token': base64.b64encode(bytes(f'{email}:{password}', 'utf-8')),
            }, HTTP_200_OK)
        else:
            return Response(None, HTTP_403_FORBIDDEN)


class LogoutView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response(None, HTTP_200_OK)


class UserMeView(RetrieveAPIView):
    serializer_class = MeSerializer

    def get_object(self):
        return self.request.user