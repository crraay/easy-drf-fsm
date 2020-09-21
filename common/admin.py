from django.contrib import admin
from fsm_admin.mixins import FSMTransitionMixin

from .models import Task


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
