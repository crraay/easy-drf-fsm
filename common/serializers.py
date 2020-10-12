from rest_framework import serializers
from easy_drf_fsm import AvailableTransitionsFieldMixin, AllTransitionsFieldMixin

from .models import Task, Purchase


class TaskSerializer(
    serializers.ModelSerializer,
    AvailableTransitionsFieldMixin,
    AllTransitionsFieldMixin,
):
    # TODO переместить в конфиг миксина
    state_field_name = 'state'
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


class PurchaseSerializer(
    serializers.ModelSerializer,
    AvailableTransitionsFieldMixin,
    AllTransitionsFieldMixin,
):
    state_field_name = 'status'
    available_transitions = serializers.SerializerMethodField()
    all_transitions = serializers.SerializerMethodField()

    class Meta:
        model = Purchase
        fields = (
            'guid',
            'title',
            'cancel_comment',
            'payment_info',
            'status',
            'available_transitions',
            'all_transitions',
        )
        read_only_fields = (
            'status',
            'cancel_comment',
            'payment_info',
            'available_transitions',
            'all_transitions',
        )