import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django_fsm import FSMField, transition


# TODO почистить миграции
# TODO сделать fixture
class Purchase(models.Model):
    STATUS_CREATED = 'created'
    STATUS_CANCELLED = 'cancelled'
    STATUS_PAID = 'paid'
    STATUS_DELIVERED = 'delivered'
    STATUS_CHOICES = (
        (STATUS_CREATED, 'Created'),
        (STATUS_CANCELLED, 'Cancelled'),
        (STATUS_PAID, 'Paid'),
        (STATUS_DELIVERED, 'Delivered'),
    )

    guid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    title = models.CharField(
        max_length=100,
    )
    status = FSMField(
        default=STATUS_CREATED,
        choices=STATUS_CHOICES,
        protected=True,
    )
    payment_info = models.CharField(
        max_length=100,
        blank=True,
    )
    cancel_comment = models.CharField(
        max_length=100,
        blank=True,
    )
    last_change_by = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self):
        return 'Purchase {}'.format(self.pk)

    @transition(
        field=status,
        source=STATUS_CREATED,
        target=STATUS_PAID,
        custom=({'button_name': 'Pay'}),
    )
    def pay(self, payment_info='some info', **kwargs):
        self.last_change_by = kwargs['by']
        self.payment_info = payment_info

    @transition(
        field=status,
        source=[STATUS_CREATED, STATUS_PAID],
        target=STATUS_CANCELLED,
        custom=({'button_name': 'Cancel'}),
    )
    def cancel(self, comment='wrong size', **kwargs):
        self.last_change_by = kwargs['by']
        self.cancel_comment = comment

    @transition(
        field=status,
        source=STATUS_PAID,
        target=STATUS_DELIVERED,
        custom=({'button_name': 'DELIVER'}),
    )
    def deliver(self, **kwargs):
        self.last_change_by = kwargs['by']
        pass

    @transition(
        field=status,
        source='*',
        target=STATUS_CREATED,
        custom=({'button_name': 'Reset'}),
    )
    def reset(self, **kwargs):
        self.last_change_by = kwargs['by']
        self.payment_info = ''
        self.cancel_comment = ''
