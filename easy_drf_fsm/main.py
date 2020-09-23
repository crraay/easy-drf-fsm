from rest_framework import decorators, response, serializers
from django_fsm import TransitionNotAllowed

from .serializers import TransitionSerializer
from .utils import get_all_transitions, get_available_transitions


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

            arguments = validated_data['arguments']
            handler(user=self.context['request'].user, **arguments)

        def _get_resolver_func(self, instance):
            resolver_func_name = 'get_available_user_{}_transitions'.format(state_field_name)
            resolver_func = getattr(instance, resolver_func_name, None)
            if not resolver_func:
                raise TransitionNotAllowed('Failed resolver function')
            return resolver_func

    return ProceedTransitionSerializer

# TODO check with another ViewSets
# TODO проверить с недефолтными параметрами id, state
# TODO use kwargs ???
# TODO add param: proceed_method_name, av_trans_method_name
# TODO RENAME???
def get_viewset_mixin(
        Model,
        id_field_name='id',
        state_field_name='state',
        show_available_transitions=True,
        show_all_transitions=False,
):
    proceed_transition_serializer = get_proceed_transition_serializer(Model, id_field_name, state_field_name)

    # TODO возвращать данные по дефолтному сериалайзеру?
    @decorators.action(
        detail=True,
        methods=['PUT'],
        serializer_class=proceed_transition_serializer,
    )
    def proceed_transition(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @decorators.action(
        detail=True,
        methods=['GET'],
        serializer_class=TransitionSerializer,
    )
    def available_transitions(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        data = get_available_transitions(Model, instance, user)

        return response.Response(TransitionSerializer(data, many=True).data)

    @decorators.action(
        detail=False,
        methods=['GET'],
        serializer_class=TransitionSerializer,
    )
    def all_transitions(self, request, *args, **kwargs):
        data = get_all_transitions(Model)

        return response.Response(TransitionSerializer(data, many=True).data)

    # TODO проверить работоспособность при нескольких сущностях
    class Mixin(object):
        pass

    setattr(Mixin, 'proceed_transition', proceed_transition)

    if show_available_transitions:
        setattr(Mixin, 'available_transitions', available_transitions)

    if show_all_transitions:
        setattr(Mixin, 'all_transitions', all_transitions)

    return Mixin