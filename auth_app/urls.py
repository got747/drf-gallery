from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import RegisterUserView, get_user

urlpatterns = [
    path('auth/token/',
         TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('auth/token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),
    path('auth/register/',
         RegisterUserView.as_view({'post': 'create'}),
         name="register"),
    path('auth/get_user/', get_user, name='get_user')
]
