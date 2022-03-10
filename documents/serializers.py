from rest_framework import serializers
from .models import File


class DocSerializer(serializers.ModelSerializer):
    cover = serializers.SerializerMethodField()
    class Meta:
        model = File
        fields = ("id", "cover", "name", "description", "private", "type")

    def get_cover(self, obj):
        return obj.cover.url

class DocUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ("id", "cover", "name", "description", "private", "user")
        read_only_fields = ("user",)
