from django.contrib import admin
from .models import Certificate

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('name', 'issuer', 'issue_date')
    search_fields = ('name', 'issuer')
