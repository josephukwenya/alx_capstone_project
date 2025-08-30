from django.contrib import admin
from .models import Applicant

@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
  list_display = ('user','first_name','last_name','is_submitted','email_sent','created_at')
  readonly_fields = ('created_at','updated_at')