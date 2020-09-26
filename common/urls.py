from django.conf.urls import url, include
from rest_framework import routers

from .api import TaskAPI, PurchaseAPI

router = routers.DefaultRouter()

router.register(r'task', TaskAPI, basename='task')
router.register(r'purchase', PurchaseAPI, basename='purchase')

urlpatterns = [
    url(r'^', include(router.urls)),
]