from django.db import models
from ..authentication.models import User
from ..article.models import Article
from app.api.models import BaseModel


class LikeDislike(BaseModel):
    # Here to be a followee/r you must be in the user table ie you have an account
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_like"
    )  # the author here already has an account
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="article_like"
    )  # here again, the article id used to relate.
    isliked = models.BooleanField(default=False)
    isdisliked = models.BooleanField(default=False)
