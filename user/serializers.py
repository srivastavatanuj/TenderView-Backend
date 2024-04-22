from rest_framework import serializers
from .models import User, Subscription
from rest_framework.response import Response


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=8, max_length=68, write_only=True)

    class Meta:
        model = User
        fields = ["fullName", "phone", 
                  "companyName", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["fullName", 
                  "companyName",]

    def update(self, instance, validated_data):
        instance.fullName = validated_data.get('fullName')
        instance.companyName = validated_data.get('companyName')
        # instance.email = validated_data.get('email')
        # if validated_data['profilePic'] is not None:
        #     instance.profilePic.delete(True)
        #     instance.profilePic = validated_data['profilePic']
        instance.save()
        return instance


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ["user", "state", "startDate", "endDate"]
        read_only_fields = ["startDate", "endDate", "user"]

    def create(self, validated_data):
        user = validated_data['user']
        if Subscription.objects.filter(user=user).exists():
            raise serializers.ValidationError("demo not available")
        return Subscription.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.endDate=validated_data['endDate']
        instance.save()
        return instance


