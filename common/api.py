from rest_framework import viewsets
from easy_drf_fsm import get_viewset_mixin

from .serializers import TaskSerializer
from .models import Task

viewset_mixin = get_viewset_mixin(
    Task,
    show_available_transitions=True,
    show_all_transitions=True
)


class TaskAPI(
    viewsets.ModelViewSet,
    viewset_mixin
):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

