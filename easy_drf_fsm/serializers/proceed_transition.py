from rest_framework import serializers
from django_fsm import TransitionNotAllowed


# TODO add additional fields(comment) param
def get_proceed_transition_serializer(
        Model,
        id_field_name='id',
        state_field_name='state',
):
    class ProceedTransitionSerializer(serializers.ModelSerializer):
        arguments = serializers.DictField(required=False)

        class Meta:
            model = Model
            fields = (
                id_field_name,
                state_field_name,
                'arguments',
            )

        def create(self, validated_data):
            raise PermissionError()

        # TODO rewrite it
        def update(self, instance, validated_data):
            try:
                self._transition(instance, validated_data.get(state_field_name, None), validated_data)
            except TransitionNotAllowed as e:
                raise serializers.ValidationError({'transition': [str(e)]})
            instance.save()
            return instance

        def _transition(self, instance, new_state, validated_data):
            handler_name = None
            resolver_func = self._get_resolver_func(instance)
            current_state = getattr(instance, state_field_name, None)

            for t in resolver_func(self.context['request'].user):
                if t.target == new_state and t.source == current_state:
                    handler_name = t.name
                    break
            if not handler_name:
                raise TransitionNotAllowed('Unavailable state')
            handler = getattr(instance, handler_name)

            # TODO
            arguments = validated_data['arguments']
            handler(user=self.context['request'].user, **arguments)

        def _get_resolver_func(self, instance):
            resolver_func_name = 'get_available_user_{}_transitions'.format(state_field_name)
            resolver_func = getattr(instance, resolver_func_name, None)
            if not resolver_func:
                raise TransitionNotAllowed('Failed resolver function')
            return resolver_func

    return ProceedTransitionSerializer
