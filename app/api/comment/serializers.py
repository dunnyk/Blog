from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):

    comment = serializers.CharField(required=True, allow_null=False)# the box for email field should not be empty

    author =  serializers.CharField(read_only=True)

    article = serializers.CharField(read_only=True)

    class Meta:
        model = Comment#this refers to model class
        fields = ('article','author','comment')



class CommentRetrieveSerializer(serializers.ModelSerializer):

    comment = serializers.CharField(required=True, allow_null=False)# the box for email field should not be empty
    author =  serializers.CharField(read_only=True)

    #Here we put comment and author, we leave out article because we are commenting about it.
    #meaning we already heve it.no need to put it here
    class Meta:#Meta class just tells which models to interact with and what fields to take.
        model = Comment#this refers to model class
        fields = ('author','comment')
