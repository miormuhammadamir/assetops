from django.contrib.auth import get_user_model
from rest_framework import serializers
from operations.models import Asset, WorkOrder, MaintenancePlan
from operations.permissions import has_role

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['id', 'code', 'name', 'location', 'description', 'status',
                  'criticality', 'next_maintenance', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class WorkOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrder
        fields = ['id', 'asset', 'title', 'description', 'priority', 'status',
                  'assigned_to', 'created_by', 'resolution_notes', 'created_at',
                  'updated_at', 'completed_at']
        read_only_fields = ['id', 'status', 'created_by', 'resolution_notes',
                            'created_at', 'updated_at', 'completed_at']

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request')
        if request and not has_role(request.user, 'Admin', 'Supervisor'):
            # Ignore submitted assignment before validating user PKs.
            fields['assigned_to'].read_only = True
        return fields

    def validate_assigned_to(self, user):
        if user is not None and (not user.is_active or not has_role(user, 'Technician')):
            raise serializers.ValidationError('Assign an active technician.')
        return user

    def validate(self, attrs):
        actor = self.context['request'].user
        if not has_role(actor, 'Admin', 'Supervisor'):
            # A technician never controls assignment, including through a forged request.
            attrs['assigned_to'] = actor
        return attrs

class MaintenancePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenancePlan
        fields = ['id', 'asset', 'title', 'instructions', 'interval_days',
                  'next_due', 'is_active', 'priority', 'assigned_to',
                  'created_by', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

    def validate_interval_days(self, value):
        if not 1 <= value <= 3650:
            raise serializers.ValidationError('Interval must be between 1 and 3650 days.')
        return value

    def validate_assigned_to(self, user):
        if user is not None and (not user.is_active or not has_role(user, 'Technician')):
            raise serializers.ValidationError('Assign an active technician.')
        return user

class StatusTransitionSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=WorkOrder.Status.choices)
    note = serializers.CharField(required=False, allow_blank=True, max_length=1000)

class ResolutionSerializer(serializers.Serializer):
    resolution_notes = serializers.CharField(allow_blank=True)
