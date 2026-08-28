from django.contrib import admin
from .models import Education

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'institution', 'start_date')
    search_fields = ('degree', 'institution')
