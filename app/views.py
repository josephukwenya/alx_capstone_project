from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.core.mail import send_mail
import cloudinary.uploader

from .models import Applicant
from .serializers import ApplicantSerializer, ApplicantUpdateSerializer
from .permissions import IsOwnerOrAdmin

from rest_framework import generics, permissions
from .serializers import UserRegisterSerializer
from django.contrib.auth.models import User

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

class ApplicantViewSet(viewsets.ModelViewSet):
  queryset = Applicant.objects.select_related('user').all()
  permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

  def get_serializer_class(self):
    if self.action in ['partial_update', 'update']:
      return ApplicantUpdateSerializer
    return ApplicantSerializer

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)

  def get_queryset(self):
    user = self.request.user
    if user.is_staff:
      return super().get_queryset()
    return Applicant.objects.filter(user=user)


  @action(detail=True, methods=['post'], url_path='submit')
  def submit(self, request, pk=None):
    applicant = self.get_object()
    if applicant.is_submitted:
      return Response({'detail':'Already submitted.'}, status=status.HTTP_400_BAD_REQUEST)

    required = ['first_name','last_name','resume','profile_picture']
    missing = [f for f in required if not getattr(app, f)]
    if missing:
      return Response({'detail': f'Missing fields: {missing}'}, status=status.HTTP_400_BAD_REQUEST)

      applicant.is_submitted = True
      applicant.step = 99
      applicant.save()

      try:
        send_mail(
          subject='Application submitted',
          message=f'Hi {applicant.first_name}, your application has been received.',
          from_email=settings.DEFAULT_FROM_EMAIL,
          recipient_list=[applicant.user.email],
          fail_silently=False,
      )
        applicant.email_sent = True
        applicant.save()
      except Exception:
        pass
      return Response({'detail':'Submitted.'}, status=status.HTTP_200_OK)