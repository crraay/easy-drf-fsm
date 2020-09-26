from rest_framework import serializers

from .. import TransitionSerializer
from easy_drf_fsm.utils import get_all_transitions


class AllTransitionsFieldMixin(metaclass=serializers.SerializerMetaclass):
    def get_all_transitions(self, instance):
        field = getattr(self.Meta.model, self.state_field_name).field
        data = get_all_transitions(self.Meta.model, field)

        return TransitionSerializer(data, many=True).data
