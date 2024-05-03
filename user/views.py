from user.models import *
from rest_framework import generics, permissions, status
from .models import *
from rest_framework.response import Response
from .serializers import UserSerializer, UserUpdateSerializer, SubscriptionSerializer
from django.shortcuts import get_object_or_404

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.conf import settings
import datetime


def dateToTimestamp(user):
    date_str = user.get_endDate()
    time_obj = datetime.time(23, 59, 59)
    datetime_obj = datetime.datetime.combine(date_str,time_obj)
    return datetime_obj.timestamp()



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):   
        

        token = super().get_token(user)

        sub=Subscription.objects.filter(user=user)

        token["userData"]={
            'user_lastLogin':user.last_login.timestamp(),
            'isActive':dateToTimestamp(sub[0])>datetime.datetime.now().timestamp() if sub else "",
        }
      
 
        token['customData']={ 
            "/tenders": {"states":sub[0].get_states()} if sub.exists() else [],
              
        }
        token['iss']="TenderView Api"

        return token


class MyTokenRefreshSerializer(TokenRefreshSerializer):

    def validate(self, attrs):

        refresh = self.token_class(attrs["refresh"])
        userId = refresh.payload['user_id']
        user=User.objects.get(id=userId)
        sub=Subscription.objects.filter(user=user)

        refresh.payload["userData"]={
            'user_lastLogin':user.last_login.timestamp(),
            'isActive':dateToTimestamp(sub[0])>datetime.datetime.now().timestamp() if sub else "",
        }
        

        refresh.payload['customData']={ 
            "/tenders": {"states":sub[0].get_states()} if sub.exists() else [],
                 
        }

        data = {"access": str(refresh.access_token)}

        return data


class RegisterUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class GetUserData(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        userId = self.request.user.id
        return User.objects.filter(pk=userId)


class UpdateUserData(generics.RetrieveUpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        userId = self.request.user.id
        return User.objects.filter(pk=userId)

    def perform_update(self, serializer):
        serializer.save()


class RequestDemo(generics.ListCreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, endDate=timezone.now(
        ).date()+timezone.timedelta(days=3))


class Subscribe(generics.UpdateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        try:
            instance=Subscription.objects.get(user=request.user)
            serializer=self.get_serializer(instance,data = request.data)
        except:
            serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save(endDate = timezone.now().date() + timezone.timedelta(days=365),user=request.user)


        return Response(serializer.data)


class RenewSubscription(generics.UpdateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self,request):
        instance=Subscription.objects.get(user=request.user)
        if instance.endDate-datetime.date.today()>datetime.timedelta(days=7):
            return Response({"error":"Unable to renew"},status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(endDate = instance.get_endDate() + timezone.timedelta(days=365),user=request.user)


        return Response(serializer.data)
