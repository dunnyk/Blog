from django.urls import path
from .views import CreateArticleAPIView, EditUpdateArticleApiView

urlpatterns = [
    path("", CreateArticleAPIView.as_view(), name="article"),
    path(
        "update/<str:article_id>",
        EditUpdateArticleApiView.as_view(),
        name="article-update",
    ),
]
