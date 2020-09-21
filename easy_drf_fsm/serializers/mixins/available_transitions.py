from rest_framework import serializers

from easy_drf_fsm.utils import get_available_transitions


# TODO put in init func ??? add params: result_name,
# TODO make automatic ???
class AvailableTransitionsMixin(metaclass=serializers.SerializerMetaclass):
    def get_available_transitions(self, instance):
        user = self.context['request'].user

        return get_available_transitions(self.Meta.model, instance, user)
