from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    short_description = models.CharField(max_length=250)
    full_description = models.TextField()
    problem_statement = models.TextField(blank=True)
    solution = models.TextField(blank=True)
    dataset_info = models.TextField(blank=True)
    ml_models = models.TextField(blank=True, help_text="Details about ML models used")
    results = models.TextField(blank=True)
    challenges = models.TextField(blank=True)
    future_improvements = models.TextField(blank=True)
    github_url = models.URLField(blank=True, null=True)
    live_demo_url = models.URLField(blank=True, null=True)
    project_image = models.ImageField(upload_to='projects/', blank=True, null=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Categories for filtering
    category = models.CharField(max_length=100, blank=True, db_index=True)

    def __str__(self):
        return self.title

class ProjectTechnology(models.Model):
    project = models.ForeignKey(Project, related_name='technologies', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name} - {self.project.title}"

class ProjectMetric(models.Model):
    project = models.ForeignKey(Project, related_name='metrics', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, help_text="e.g. Accuracy")
    value = models.CharField(max_length=100, help_text="e.g. 95%")
    
    def __str__(self):
        return f"{self.name}: {self.value} ({self.project.title})"
