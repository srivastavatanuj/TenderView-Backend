from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('<int:pk>/', GetUserData.as_view(), name='details'),
    path('<int:pk>/update/', UpdateUserData.as_view(), name='update'),
    path('request-demo/', RequestDemo.as_view(), name='demo'),
    path('subscribe/', Subscribe.as_view(), name='subscribe'),
    path('renew-subscribe/', RenewSubscription.as_view(), name='resubscribe'),
    # path('renew-subscribe/', RenewSubscription.as_view(), name='resubscribe'),
]
