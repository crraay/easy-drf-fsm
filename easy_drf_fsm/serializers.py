from rest_framework import serializers

from easy_drf_fsm.utils import get_available_transitions, get_all_transitions


class TransitionSerializer(serializers.Serializer):
    name = serializers.CharField()
    source = serializers.CharField()
    target = serializers.CharField()
    arguments = serializers.ListField()
    custom = serializers.DictField()


class AvailableTransitionsFieldMixin(metaclass=serializers.SerializerMetaclass):
    def get_available_transitions(self, instance):
        user = self.context['request'].user
        field = getattr(self.Meta.model, self.state_field_name).field
        data = get_available_transitions(field, instance, user)

        return TransitionSerializer(data, many=True).data


class AllTransitionsFieldMixin(metaclass=serializers.SerializerMetaclass):
    def get_all_transitions(self, instance):
        field = getattr(self.Meta.model, self.state_field_name).field
        data = get_all_transitions(self.Meta.model, field)

        return TransitionSerializer(data, many=True).data
