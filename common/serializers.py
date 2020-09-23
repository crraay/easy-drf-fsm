from rest_framework import serializers
from easy_drf_fsm import AvailableTransitionsFieldMixin, AllTransitionsFieldMixin

from .models import Task


class TaskSerializer(serializers.ModelSerializer, AvailableTransitionsFieldMixin, AllTransitionsFieldMixin):
    available_transitions = serializers.SerializerMethodField()
    custom_field_name = serializers.SerializerMethodField(method_name='get_all_transitions')

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'decline_comment',
            'state',
            'available_transitions',
            'custom_field_name',
        )
        read_only_fields = (
            'state',
            'decline_comment',
            'available_transitions',
            'custom_field_name',
        )
