from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Image
from .permissions import IsAdminOrOwner, IsOnlyAdmin

from .serializers import ImageSerializer, ImageCreateSerializer


class ImageViewSet(viewsets.ModelViewSet):

    default_serializer_class = ImageSerializer

    serializer_classes = {
        'list': ImageSerializer,
        'retrieve': ImageSerializer,
        'destroy': ImageSerializer,
        'create': ImageCreateSerializer,
        'update': ImageCreateSerializer,
        'partial_update': ImageCreateSerializer
    }

    action_permissions = {
        'list': (IsAdminOrOwner, ),
        'create': (permissions.IsAuthenticated, ),
        'destroy': (IsAdminOrOwner, ),
        'retrieve': (IsAdminOrOwner, ),
        'partial_update': (IsAdminOrOwner, ),
        'delete_all_entries': (IsOnlyAdmin, ),
    }

    def get_permissions(self):
        if self.action:
            return (permission()
                    for permission in self.action_permissions[self.action])
        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action,
                                           self.default_serializer_class)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_admin:
                return Image.objects.select_related('user').all()
            return Image.objects.select_related('user').filter(
                user=self.request.user)

    @action(detail=False, methods=['delete'])
    def delete_all_entries(self, request):
        """
        The endpoint deletes all records in the database and on disk
        """
        Image.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
