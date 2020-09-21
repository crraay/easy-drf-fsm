from rest_framework import serializers
from easy_drf_fsm import AvailableTransitionsMixin

from .models import Task


class TaskSerializer(serializers.ModelSerializer, AvailableTransitionsMixin):
    # TODO Объединить в один миксин?
    # available_transitions = serializers.SerializerMethodField(method_name='get_available_transitions')
    # TODO get_all_transitions ????

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'decline_comment',
            'state',
            # 'available_transitions',
        )
        read_only_fields = (
            'state',
        )

# TODO create an example with comment
