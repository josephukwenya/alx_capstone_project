from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ApplicantViewSet
from .views import UserRegisterView

router = DefaultRouter()
router.register(r'applicants', ApplicantViewSet, basename='app')

urlpatterns = [
  path('', include(router.urls)),
  path("register/", UserRegisterView.as_view(), name="register"),
]