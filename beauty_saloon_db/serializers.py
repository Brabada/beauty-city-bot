from rest_framework import serializers
from beauty_saloon_db.models import Saloon

class SaloonsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saloon
        fields = '__all__'
