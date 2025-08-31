from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Applicant

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_staff", "is_superuser"]
        read_only_fields = ["id", "is_staff", "is_superuser"]


class ApplicantSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Applicant
        fields = "__all__"
        read_only_fields = ["user", "is_submitted", "email_sent", "step"]

    def to_representation(self, instance):
        """Return Cloudinary URLs instead of file objects"""
        rep = super().to_representation(instance)
        if instance.profile_picture:
            rep["profile_picture"] = instance.profile_picture.url
        if instance.resume:
            rep["resume"] = instance.resume.url
        return rep


class ApplicantUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        # Only allow controlled updates
        fields = ["first_name", "last_name", "phone", "address", "profile_picture", "resume", "qualifications"]
