from django.contrib import admin
from django.conf.urls import url, include
from rest_framework_swagger.views import get_swagger_view

urlpatterns = [
    url(r'^api/', include('common.urls')),
    url(r'^api/docs/$', get_swagger_view()),
    url(r'^admin/', admin.site.urls),
]
