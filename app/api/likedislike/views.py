from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import LikeDislike, Article
from .serializers import LikeDislikeSerializers
from ..helpers.renderers import RequestJSONRenderer
from .helpers.like_dislike_article import like_article


class ArticleLikeApiView(generics.GenericAPIView):
    renderer_classes = (RequestJSONRenderer,)
    permission_classes = (IsAuthenticated,)
    serializer_class = LikeDislikeSerializers

    def post(self, action):
        like_article()
        return_message = {
            "message": f"You {action}d",

            }
        return Response(return_message, status.HTTP_201_CREATED)
