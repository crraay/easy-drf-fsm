# TODO вынести куда-либо?
from django_fsm import get_available_user_FIELD_transitions, get_all_FIELD_transitions
import inspect


# Вытаскиваем аргументы методов по сигнатуре
def _get_transitions(instance, transition_list):
    for t in transition_list:
        handler = getattr(instance, t.name)
        t.arguments = list(inspect.signature(handler).parameters.keys())

    return transition_list


# TODO? remove model??
def get_available_transitions(model, instance, user):
    # TODO check for existing state field
    # TODO check with another viewsets
    state_field = model.state.field

    data = get_available_user_FIELD_transitions(instance, user, state_field)

    return _get_transitions(instance, list(data))


def get_all_transitions(model):
    # TODO check for existing state field
    # TODO check with another viewsets
    state_field = model.state.field

    data = state_field.get_all_transitions(model)


    return _get_transitions(model, list(data))
