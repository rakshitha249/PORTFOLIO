import os

files = {
    'portfolio/admin.py': """from django.contrib import admin
from .models import Profile, Skill, SocialLink

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'email')
    search_fields = ('name', 'title', 'bio')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'proficiency')
    list_filter = ('category',)
    search_fields = ('name',)

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'url')
""",
    'projects/admin.py': """from django.contrib import admin
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
""",
    'experience/admin.py': """from django.contrib import admin
from .models import Experience

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('role', 'company', 'start_date', 'end_date', 'is_current')
    list_filter = ('is_current',)
    search_fields = ('role', 'company')
""",
    'education/admin.py': """from django.contrib import admin
from .models import Education

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'institution', 'start_date')
    search_fields = ('degree', 'institution')
""",
    'certificates/admin.py': """from django.contrib import admin
from .models import Certificate

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('name', 'issuer', 'issue_date')
    search_fields = ('name', 'issuer')
""",
    'contact/admin.py': """from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
"""
}

for filepath, content in files.items():
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Created all admin files.")
