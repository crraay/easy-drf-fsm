# TODO перенести сюда миксины, убрать лишние пакеты
from rest_framework import serializers


# TODO add show_arguments param
class TransitionSerializer(serializers.Serializer):
    name = serializers.CharField()
    source = serializers.CharField()
    target = serializers.CharField()
    arguments = serializers.ListField()
    custom = serializers.DictField()
