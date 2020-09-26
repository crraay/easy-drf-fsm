# TODO вынести куда-либо?
from django_fsm import get_available_user_FIELD_transitions, get_all_FIELD_transitions
import inspect


# Вытаскиваем аргументы методов по сигнатуре
# TODO убрать аргумент self в classmethod представлении
def _get_transitions(instance, transition_list):
    for t in transition_list:
        handler = getattr(instance, t.name)
        t.arguments = list(inspect.signature(handler).parameters.keys())

    return transition_list


def get_available_transitions(field, instance, user):
    data = get_available_user_FIELD_transitions(instance, user, field)

    return _get_transitions(instance, list(data))


def get_all_transitions(model, field):
    data = field.get_all_transitions(model)

    return _get_transitions(model, list(data))
