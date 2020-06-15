from top.models import Notification
from guide.util import text_html_converter


def context_initializer(request, context):
    if request.user.is_authenticated:
        notification_list = Notification.objects.filter(user=request.user)
        num_of_unread = 0
        for notification in notification_list:
            if not notification.alreadyRead:
                num_of_unread += 1

        context["num_of_unread"] = num_of_unread

    return context;
