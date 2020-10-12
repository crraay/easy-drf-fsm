from django.db import models
from django_fsm import FSMIntegerField, transition


class TaskState(object):
    NEW = 10
    ACTIVE = 20
    RESOLVED = 30
    CLOSED = 50

    RESOLVER = {
        NEW: 'New',
        ACTIVE: 'Active',
        RESOLVED: 'Resolved',
        CLOSED: 'Closed',
    }

    CHOICES = RESOLVER.items()


class Task(models.Model):
    title = models.CharField(
        max_length=100,
    )
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

    # TODO add custom fields to transitions: color
    @transition(
        field=state,
        source=TaskState.NEW,
        target=TaskState.ACTIVE,
        custom=({'button_name': 'Set as active'}),
    )
    def activate(self, **kwargs):
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
