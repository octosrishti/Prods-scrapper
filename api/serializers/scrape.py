from rest_framework import serializers
from api.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from ..models import ScrapeModel

class ScrapeSerializer(serializers.Serializer):
    """."""
    url = serializers.URLField(required=False, allow_blank=True, allow_null=True, max_length=1000)
   
class ScrapeDetailSerializer(serializers.ModelSerializer):
    """."""
    
    class Meta:
        model = ScrapeModel
        fields = '__all__'
   