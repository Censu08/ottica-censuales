from rest_framework import serializers
from .models import IntegrationLog

class IntegrationLogSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()
    
    class Meta:
        model = IntegrationLog
        fields = [
            'id', 'operation_type', 'status', 'parameters',
            'records_processed', 'records_success', 'records_failed',
            'log_messages', 'error_details', 'started_at', 'completed_at',
            'duration', 'created_at'
        ]
    
    def get_duration(self, obj):
        if obj.started_at and obj.completed_at:
            delta = obj.completed_at - obj.started_at
            return delta.total_seconds()
        return None