from rest_framework import viewsets
from easy_drf_fsm import get_viewset_mixin

from .serializers import TaskSerializer, PurchaseSerializer
from .models import Task, Purchase

task_viewset_mixin = get_viewset_mixin(
    Task,
    show_available_transitions=True,
    show_all_transitions=True
)


class TaskAPI(
    viewsets.ModelViewSet,
    task_viewset_mixin
):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()


# TODO change id_field_name
purchase_viewset_mixin = get_viewset_mixin(
    Purchase,
    state_field_name='status',
    show_available_transitions=True,
    show_all_transitions=True
)


class PurchaseAPI(
    viewsets.ModelViewSet,
    purchase_viewset_mixin,
):
    serializer_class = PurchaseSerializer
    queryset = Purchase.objects.all()

