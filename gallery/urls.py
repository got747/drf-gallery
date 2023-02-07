from rest_framework import routers
from django.urls import path, include
from .views import ImageViewSet

router = routers.SimpleRouter()
router.register('image', ImageViewSet, basename='Image')

urlpatterns = [
    path('', include(router.urls), name='image'),
    path('delete_all_entries/',
         ImageViewSet.delete_all_entries,
         name='delete_all_entries')
]
