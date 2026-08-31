from django import forms
from django.contrib import admin
from .models import Certificate

class CertificateAdminForm(forms.ModelForm):
    credential_url = forms.CharField(required=False)

    class Meta:
        model = Certificate
        fields = '__all__'

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    form = CertificateAdminForm
    list_display = ('name', 'issuer', 'issue_date')
    search_fields = ('name', 'issuer')
