from contact.models import ContactUs
from rest_framework import generics, permissions
from contact.serializers import ContactSerializer


class ContactMsgSend(generics.CreateAPIView):
    queryset = ContactUs.objects.none()
    serializer_class = ContactSerializer
    permission_classes = [permissions.AllowAny]
