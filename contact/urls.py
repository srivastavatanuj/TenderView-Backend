from django.urls import path
from .views import *

urlpatterns = [
    path("", ContactMsgSend.as_view())
]
