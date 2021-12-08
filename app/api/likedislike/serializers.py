from rest_framework import serializers
from .models import LikeDislike


class LikeDislikeSerializers(serializers.ModelSerializer):
    author = serializers.CharField(required=False)
    article = serializers.CharField(required=True)
    isliked = serializers.BooleanField(default=False)#default is false bcz users will not pass,
    isdisliked = serializers.BooleanField(default=False)


    class Meta:
        model = LikeDislike
        fields = ('author', 'article', 'isliked', 'isdisliked')
