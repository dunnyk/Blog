from rest_framework.serializers import ValidationError
from ..models import Comment


def edit_comment_get(comment_id):

    try:
        comment = Comment.objects.get(pk=comment_id)#variable name(comment) is same with name from get() in views
        return comment
    except Comment.DoesNotExist:
        raise ValidationError(
            "This Comment does not exist",
        )
