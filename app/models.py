from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError

class Applicant(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applicant")
  step = models.PositiveIntegerField(default=1)
  is_submitted = models.BooleanField(default=False)
  email_sent = models.BooleanField(default=False)

  first_name = models.CharField(max_length=100, blank=True)
  last_name = models.CharField(max_length=100, blank=True)
  phone = models.CharField(max_length=20, blank=True)
  address = models.TextField(blank=True)

  profile_picture = models.URLField(blank=True)
  resume = models.URLField(blank=True) 

  try:
    from django.db.models import JSONField as BuiltinJSONField
    qualifications = BuiltinJSONField(blank=True, null=True)
  except Exception:
    qualifications = models.TextField(blank=True)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    ordering = ["-created_at"]

  def clean(self):
    # Prevent updates when submitted (except by staff through admin or dedicated endpoint)
    if self.pk and self.is_submitted and not getattr(self, "_allow_mutation", False):
      raise ValidationError("Application is locked after submission.")

  def can_edit(self, acting_user) -> bool:
    return (acting_user.is_staff) or (acting_user == self.user and not self.is_submitted)

  def __str__(self):
    return f"Applicant<{self.user.username}>"