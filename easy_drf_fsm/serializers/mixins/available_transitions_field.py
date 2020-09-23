from rest_framework import serializers

from .. import TransitionSerializer
from easy_drf_fsm.utils import get_available_transitions


class AvailableTransitionsFieldMixin(metaclass=serializers.SerializerMetaclass):
    def get_available_transitions(self, instance):
        user = self.context['request'].user
        data = get_available_transitions(instance.__class__, instance, user)

        return TransitionSerializer(data, many=True).data
