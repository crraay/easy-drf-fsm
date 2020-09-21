from django.db import models
from django_fsm import FSMField


# TODO RENAME
class IssueStatus(object):
    NEW = 'NEW'
    ACTIVE = 'ACTIVE'
    RESOLVED = 'RESOLVED'
    CLOSED = 'CLOSED'


# TODO RENAME
class Issue(models.Model):
    title = models.CharField(
        max_length=100,
        null=False
    )
    status = FSMField(
        default=IssueStatus.NEW,
        choices=IssueStatus.CHOICES,
        protected=True
    )
