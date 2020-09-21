from django.db import models
from django_fsm import FSMIntegerField, transition


class TaskState(object):
    # TODO избавиться от цифр
    NEW = 10
    ACTIVE = 20
    RESOLVED = 30
    CLOSED = 50

    # TODO ???
    RESOLVER = {
        NEW: 'New',
        ACTIVE: 'Active',
        RESOLVED: 'Resolved',
        CLOSED: 'Closed',
    }

    CHOICES = RESOLVER.items()


# TODO rename to simple task??
class Task(models.Model):
    title = models.CharField(
        max_length=100,
        # TODO check for null/blank difference
        # blank=False
    )
    # description = models.TextField()
    state = FSMIntegerField(
        default=TaskState.NEW,
        choices=TaskState.CHOICES,
        protected=True
    )
    decline_comment = models.CharField(
        max_length=100,
        blank=True
    )

    def __str__(self):
        return 'Task {}'.format(self.pk)

    # TODO
    # add custom fields to transitions: color
    # add args to methods
    @transition(
        field=state,
        source=TaskState.NEW,
        target=TaskState.ACTIVE,
        custom=({'button_name': 'Set as active'}),
    )
    def activate(self, test, **kwargs):
        pass

    @transition(
        field=state,
        source=TaskState.ACTIVE,
        target=TaskState.RESOLVED,
        custom=({'button_name': 'Resolve'}),
    )
    def resolve(self, **kwargs):
        pass

    @transition(
        field=state,
        source=TaskState.RESOLVED,
        target=TaskState.ACTIVE,
        custom=({'button_name': 'Decline'}),
    )
    def decline(self, comment, **kwargs):
        self.decline_comment = comment

    @transition(
        field=state,
        source=TaskState.RESOLVED,
        target=TaskState.CLOSED,
        custom=({'button_name': 'Close'}),
    )
    def close(self, **kwargs):
        pass
