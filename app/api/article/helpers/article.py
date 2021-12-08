from rest_framework.serializers import ValidationError
from ..models import Article


def retrieve_article(article_id):
    """Function for retrieving article

    Arg:
        None
    Return:
        None
    Raise:
        None
    """
    try:
        article = Article.objects.get(pk=article_id)
        return article
    except Article.DoesNotExist:
        raise ValidationError(
            "The article you want to delete does not exist"
        )
