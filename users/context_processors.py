from .models import *


def unreadMessagesCount(request):

    if request.user.is_authenticated:
        profile=request.user.profile
        messageRequests=profile.messages.all()
        unreadCount=messageRequests.filter(is_read=False).values('name').count()

        return{'unreadCount': unreadCount}
    else:
        return{'unreadCount': None}