from rest_framework import serializers

from .. import TransitionSerializer
from easy_drf_fsm.utils import get_all_transitions


class AllTransitionsFieldMixin(metaclass=serializers.SerializerMetaclass):
    def get_all_transitions(self, instance):
        user = self.context['request'].user
        data = get_all_transitions(instance.__class__)

        return TransitionSerializer(data, many=True).data
