from django.contrib import admin
from .models import Project, ProjectTechnology, ProjectMetric

class ProjectTechnologyInline(admin.TabularInline):
    model = ProjectTechnology
    extra = 1

class ProjectMetricInline(admin.TabularInline):
    model = ProjectMetric
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_published', 'created_at')
    list_filter = ('is_published', 'category')
    search_fields = ('title', 'short_description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectTechnologyInline, ProjectMetricInline]
