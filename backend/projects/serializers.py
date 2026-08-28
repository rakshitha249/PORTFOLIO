from rest_framework import serializers
from .models import Project, ProjectTechnology, ProjectMetric

class ProjectTechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTechnology
        fields = ['id', 'name']

class ProjectMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMetric
        fields = ['id', 'name', 'value']

class ProjectSerializer(serializers.ModelSerializer):
    technologies = ProjectTechnologySerializer(many=True, read_only=True)
    metrics = ProjectMetricSerializer(many=True, read_only=True)
    
    class Meta:
        model = Project
        fields = '__all__'
