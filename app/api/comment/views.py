
from rest_framework import status
from rest_framework import generics, mixins
from ..helpers.renderers import RequestJSONRenderer
from .serializers import CommentSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Article
from .helpers.edit_comment import edit_comment_get



class CreateCommentAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)#Here user currently authenticated is taken dynamically.
    renderer_classes = (RequestJSONRenderer,)
    serializer_class = CommentSerializer

    def post(self, request):
        """
        Handle user creating comments
        """
        comment = request.data


        serializer = self.serializer_class(data=comment)
        serializer.is_valid(raise_exception=True)
        article_id=request.data['article']
        article = Article.objects.get(pk=article_id)
        serializer.save(author=request.user, article=article)#user is a method in class request, and one currently logged in.
        #the tokens generated was unique depeding with who is logged in.
        data = serializer.data
        return_message = {
            "message":"Comment created successfully",
            "data":data
        }
        return Response(return_message, status=status.HTTP_201_CREATED)


class EditCommentApiView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)#Here user currently authenticated is taken dynamically.
    renderer_classes = (RequestJSONRenderer,)#AllowAny here if logged in or not logged in you are allowed to comment.
    serializer_class = CommentSerializer

    def patch(self, request, comment_id):#patch mostly is updating
        comment = Article.objects.get(pk=comment_id)
        data = request.data

        serializer = self.serializer_class(comment, data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return_message = {
            "message":"Comment updated successfully",
            "data": serializer.data
        }

        return Response(return_message, status=status.HTTP_201_CREATED)


    def get(self, request, comment_id):
        comment = edit_comment_get(comment_id)#variable name(comment) is same with name from edit_comment_get()
        serializer = self.serializer_class(comment)
        data = serializer.data

        return_message = {
            "message":"Comment retrieved succefully",
            "data":data
        }
        return Response(return_message, status=status.HTTP_200_OK)



    def delete(self, request, comment_id):
        comment = edit_comment_get(comment_id)
        comment.delete()
        serializer = self.serializer_class(comment)
        data = serializer.data

        return_message = {
            "message":"Comment deleted succefully",
            "data":data#shows the comment that is deleted
        }
        return Response(return_message, status=status.HTTP_200_OK)
