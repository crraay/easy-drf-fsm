from django.conf.urls import url, include
from rest_framework import routers

from .api import TaskAPI

router = routers.DefaultRouter()

router.register(r'task', TaskAPI, basename='task')

urlpatterns = [
    url(r'^', include(router.urls)),
]