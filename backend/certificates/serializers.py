from rest_framework import serializers
from .models import Certificate

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request and representation.get('credential_url'):
            url = representation['credential_url']
            if url.startswith('/'):
                representation['credential_url'] = request.build_absolute_uri(url)
        return representation
