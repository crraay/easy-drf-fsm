from rest_framework import serializers

from .. import TransitionSerializer
from easy_drf_fsm.utils import get_available_transitions


class AvailableTransitionsFieldMixin(metaclass=serializers.SerializerMetaclass):
    def get_available_transitions(self, instance):
        user = self.context['request'].user
        field = getattr(self.Meta.model, self.state_field_name).field
        data = get_available_transitions(field, instance, user)

        return TransitionSerializer(data, many=True).data
