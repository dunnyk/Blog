from ...article.models import Article
from ..models import LikeDislike
from ..serializers import LikeDislikeSerializers


def like_article(request, action):
    data = request.data
    like_dislike_action = f"is{action}d"  # isdisliked
    like_dislike_mapper = {"isdisliked": "isliked", "isliked": "isdisliked"}
    # querrying the database using the filter(article=data['article'], author=request.user) passed at insomnia
    like_status = LikeDislike.objects.filter(
        article=data["article"], author=request.user
    ).first()
    if not like_status:  # meaning no item/instance in db
        data[like_dislike_action] = True
        serializer = LikeDislikeSerializers(data=data)
        serializer.is_valid(raise_exception=True)
        article = Article.objects.get(id=data["article"])
        serializer.save(author=request.user, article=article)
    else:
        oppo_like_dislike_action = like_dislike_mapper[like_dislike_action]  # isLiked
        oppo_like_dislike = getattr(like_status, oppo_like_dislike_action)  # true
        like_dislike = getattr(like_status, like_dislike_action)  # false

        if oppo_like_dislike and not like_dislike:
            setattr(like_status, like_dislike_action, not like_dislike)
            setattr(like_status, oppo_like_dislike_action, not oppo_like_dislike)
        else:
            setattr(like_status, like_dislike_action, not like_dislike)

        like_status.save()
