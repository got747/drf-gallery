from rest_framework import status, mixins, viewsets
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import UserRegistrSerializer, UserSerializer


class RegisterUserView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (AllowAny, )
    http_method_names = ['post']
    serializer_class = UserRegistrSerializer


@api_view(['get'])
@permission_classes([IsAuthenticated])
def get_user(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(data=serializer.data, status=status.HTTP_200_OK)
