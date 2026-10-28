
from rest_framework import serializers
from .models import Asset


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = [
            "id",
            "code",
            "name",
            "location",
            "description",
            "status",
            "criticality",
        ]
        read_only_fields = ["id"]
