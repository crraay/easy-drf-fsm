from rest_framework import decorators, response, serializers
from django_fsm import TransitionNotAllowed

from .serializers import TransitionSerializer
from .utils import get_available_transitions, get_all_transitions


def get_proceed_transition_serializer(
        Model,
        id_field_name='id',
        state_field_name='state',
        # do not forget to make a keyword("by") param or **kwargs when using
        pass_user_argument=False,
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
                if t.target == new_state and (t.source == current_state or t.source == '*'):
                    handler_name = t.name
                    break
            if not handler_name:
                raise TransitionNotAllowed('Unavailable {}'.format(state_field_name))
            handler = getattr(instance, handler_name)

            arguments = validated_data['arguments']

            if pass_user_argument:
                handler(by=self.context['request'].user, **arguments)
            else:
                handler(**arguments)

        def _get_resolver_func(self, instance):
            resolver_func_name = 'get_available_user_{}_transitions'.format(state_field_name)
            resolver_func = getattr(instance, resolver_func_name, None)
            if not resolver_func:
                raise TransitionNotAllowed('Failed resolver function')
            return resolver_func

    return ProceedTransitionSerializer


# TODO RENAME???
def get_viewset_mixin(
        Model,
        id_field_name='id',
        state_field_name='state',
        enable_proceed_method=True,
        proceed_method_name='proceed_transition',
        enable_available_transitions_method=False,
        available_transitions_method_name='available_transitions',
        enable_all_transitions_method=False,
        all_transitions_method_name='all_transitions',
        pass_user_argument=False,
):
    proceed_transition_serializer = get_proceed_transition_serializer(
        Model,
        id_field_name,
        state_field_name,
        pass_user_argument
    )

    class Mixin(object):
        if enable_proceed_method:
            # TODO возвращать данные по дефолтному сериалайзеру?
            @decorators.action(
                detail=True,
                methods=['PUT'],
                serializer_class=proceed_transition_serializer,
                url_name=proceed_method_name,
                url_path=proceed_method_name,
            )
            def proceed_transition_method(self, request, *args, **kwargs):
                return self.update(request, *args, **kwargs)

        if enable_available_transitions_method:
            @decorators.action(
                detail=True,
                methods=['GET'],
                serializer_class=TransitionSerializer,
                url_name=available_transitions_method_name,
                url_path=available_transitions_method_name,
            )
            def available_transitions(self, request, *args, **kwargs):
                user = request.user
                instance = self.get_object()
                field = getattr(Model, state_field_name).field
                data = get_available_transitions(field, instance, user)

                return response.Response(TransitionSerializer(data, many=True).data)

        if enable_all_transitions_method:
            @decorators.action(
                detail=False,
                methods=['GET'],
                serializer_class=TransitionSerializer,
                url_name=all_transitions_method_name,
                url_path=all_transitions_method_name,
            )
            def all_transitions(self, request, *args, **kwargs):
                field = getattr(Model, state_field_name).field
                data = get_all_transitions(Model, field)

                return response.Response(TransitionSerializer(data, many=True).data)

    return Mixin
