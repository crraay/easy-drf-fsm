from django.contrib import admin
from fsm_admin.mixins import FSMTransitionMixin

from .models import Task, Purchase


@admin.register(Task)
class TaskAdmin(FSMTransitionMixin, admin.ModelAdmin):
    list_display = (
        '__str__',
    )
    fields = (
        'id',
        'title',
        # 'description',
        'state',
        'decline_comment',
    )
    readonly_fields = (
        'id',
        'state',
        'decline_comment',
    )


@admin.register(Purchase)
class PurchaseAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fsm_field = ['status', ]
    list_display = (
        '__str__',
    )
    fields = (
        'guid',
        'title',
        # 'description',
        'status',
        'cancel_comment',
        'payment_info',
        'last_change_by',
    )
    readonly_fields = (
        'guid',
        'status',
        'cancel_comment',
        'payment_info',
        'last_change_by',
    )
