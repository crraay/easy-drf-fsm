from django.contrib import admin
from fsm_admin.mixins import FSMTransitionMixin

from .models import Task, Purchase


@admin.register(Task)
class TaskAdmin(FSMTransitionMixin, admin.ModelAdmin):
    list_display = (
        '__str__',
    )
    fields = (
        'title',
        # 'description',
        'state',
        'decline_comment',
    )
    readonly_fields = (
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
        'title',
        # 'description',
        'status',
        'cancel_comment',
        'payment_info',
    )
    readonly_fields = (
        'status',
        'cancel_comment',
        'payment_info',
    )
