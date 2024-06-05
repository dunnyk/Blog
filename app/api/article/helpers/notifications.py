from django.conf import settings

from ...social.models import Social
from ...authentication.tasks import send_mail_


def send_email_notification(user, recipient):
    """
        This user is the person logged in, author of article,
        recipient is the follower.
        notification will be sent whether on/off net.
    """
    subject = 'New article'
    body = f"{user.username} has Posted a new article"
    message = f'{user.username} You cannot afford to miss this'
    send_mail_.delay(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_SENDER,
        recipient_list=[recipient],
        html_message=body,
        fail_silently=False,)


def send_notifications(author):
    """Fuction that sends notifications

    Arg:
        None
    Return:
        None
    Riase:
        None
    """
    followers = Social.objects.filter(followee=author.id)
    for follower in followers:
        send_email_notification(author, follower.follower.email)
