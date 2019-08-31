from .models import Message


def messages_for_user(request):
    if request.user.is_authenticated:
        messages = Message.objects.\
            filter(recipient=request.user).\
            filter(status=Message.ST_WAITNG)
        return {'messages_for_user':messages}
    return {}