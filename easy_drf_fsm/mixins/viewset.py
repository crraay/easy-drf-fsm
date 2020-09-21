from rest_framework import decorators, response

from ..serializers import get_proceed_transition_serializer, TransitionSerializer
# from .. import utils
from ..utils import get_all_transitions, get_available_transitions

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

    @decorators.action(
        detail=True,
        methods=['PUT'],
        serializer_class=proceed_transition_serializer,
        name='proceed_transition',
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
        user = request.user
        instance = Model.objects.get(pk=1)
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
