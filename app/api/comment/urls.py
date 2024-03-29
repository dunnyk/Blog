from django.urls import path
from .views import CreateCommentAPIView, EditCommentApiView

urlpatterns = [
    path('', CreateCommentAPIView.as_view(), name='comment'),
    path('update/<str:comment_id>', EditCommentApiView.as_view(), name='comment-update'),
]