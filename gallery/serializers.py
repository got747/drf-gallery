from rest_framework import serializers
from .models import Image


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = "__all__"


class ImageCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ('id', 'title', 'image')
