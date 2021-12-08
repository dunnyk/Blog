

from django.urls import path
from .views import ArticleLikeApiView

urlpatterns = [
    path('<str:action>', ArticleLikeApiView.as_view(), name='like-dislike'),
]
