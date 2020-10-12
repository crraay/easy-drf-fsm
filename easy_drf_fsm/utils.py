from django_fsm import get_available_user_FIELD_transitions
import inspect


# Get method's arguments by signature
def _get_transitions(instance, transition_list):
    for t in transition_list:
        handler = getattr(instance, t.name)
        arguments = list(inspect.signature(handler).parameters.keys())

        # if method is not bound - remove first(self) argument
        if not hasattr(handler, '__self__'):
            t.arguments = arguments[1:]
        else:
            t.arguments = arguments

    return transition_list


def get_available_transitions(field, instance, user):
    data = get_available_user_FIELD_transitions(instance, user, field)

    return _get_transitions(instance, list(data))


def get_all_transitions(model, field):
    data = field.get_all_transitions(model)

    return _get_transitions(model, list(data))
