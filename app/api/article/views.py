from rest_framework import status
from rest_framework import generics, mixins
from ..helpers.renderers import RequestJSONRenderer
from .serializers import ArticleSerializer, ArticleRetrieverSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Article
from .helpers.notifications import send_notifications
from .helpers.article import retrieve_article


class CreateArticleAPIView(generics.CreateAPIView):
    permission_classes = (
        # IsAuthenticated,
    )  # Here user currently authenticated is taken dynamically.
    renderer_classes = (RequestJSONRenderer,)
    serializer_class = ArticleSerializer

    # Post and get should be put together because they share one class.
    # Both of them don't require an id for post of get all.
    def post(self, request):
        """
        Handle user posts
        """
        article = request.data

        serializer = self.serializer_class(data=article)
        serializer.is_valid(raise_exception=True)

        serializer.save(
            author=request.user
        )  # models will tell you what to put bcz of Foreigh Key r/shp.
        data = serializer.data

        # send notifications
        # get the author
        # fetch all the followers
        send_notifications(request.user)

        return_message = {"message": "notifications sent successfully", "data": data}
        return Response(return_message, status=status.HTTP_201_CREATED)

    def get(self, request):
        article = Article.objects.all()
        serializer = self.serializer_class(article, many=True)
        return_message = {
            "message": "Article retrieved successfully",
            "data": serializer.data,
        }
        return Response(return_message, status=status.HTTP_200_OK)


class EditUpdateArticleApiView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    permission_classes = (
        IsAuthenticated,
    )  # Here user currently authenticated is taken dynamically.
    renderer_classes = (
        RequestJSONRenderer,
    )  # AllowAny here if logged in or not logged in you are allowed to comment.
    serializer_class = ArticleSerializer
    # In here patch, get and delete are done on specific articles and therefore a unique article_id is required
    # For this reason, they should be put in the sama class.

    def patch(self, request, article_id):  # patch is updating
        article = Article.objects.get(pk=article_id)
        data = request.data
        # Now check if the data required has set qualities, using serializer
        serializer = self.serializer_class(article, data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)  # currently logged in.
        return_message = {
            "message": "Article updated successfully",
            "data": serializer.data,
        }

        return Response(return_message, status=status.HTTP_201_CREATED)

    def get(self, request, article_id):
        article = retrieve_article(article_id)
        serializer = ArticleRetrieverSerializer(article)
        data = (
            serializer.data
        )  # This refers to the instance/object of class(can be accessed thr' serializer.data)
        return_message = {"message": "Article retrieved succefully", "data": data}
        return Response(return_message, status=status.HTTP_200_OK)

    def delete(self, request, article_id):
        article = retrieve_article(article_id)

        article.delete()
        serializer = self.serializer_class(article)
        data = serializer.data

        return_message = {
            "message": "Article deleted succefully",
            "data": data,  # shows the article that is deleted
        }
        return Response(return_message, status=status.HTTP_200_OK)
