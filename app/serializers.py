from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Applicant

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ["id", "username", "email", "is_staff", "is_superuser"]
    read_only_fields = ["id", "is_staff", "is_superuser"]

class ApplicantSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)

class Meta:
  model = Applicant
  fields = [
    "id", "user", "step", "is_submitted", "email_sent",
    "first_name", "last_name", "phone", "address",
    "profile_picture", "resume", "qualifications",
    "created_at", "updated_at",
    ]

class ApplicantUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        # Allow only specific fields to be updated
        fields = ["first_name", "last_name", "email", "phone_number"]