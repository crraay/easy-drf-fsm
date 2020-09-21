from rest_framework import serializers


class TransitionSerializer(serializers.Serializer):
    name = serializers.CharField()
    source = serializers.IntegerField()
    target = serializers.IntegerField()
    arguments = serializers.ListField()
    custom = serializers.DictField()
