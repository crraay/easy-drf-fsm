from rest_framework import viewsets
from easy_drf_fsm import get_viewset_mixin

from .serializers import TaskSerializer
from .models import Task

# from rest_framework import decorators, response
#
# @decorators.action(detail=True, methods=['GET'])
# def test2(self, request, *args, **kwargs):
#     user = request.user
#     instance = self.get_object()
#
#     return response.Response('123')
#
# class Mixin(object):
#     pass
#
# setattr(Mixin, 'test2', test2)

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

