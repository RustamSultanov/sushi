from .models import Message


def messages_for_user(request):
    if request.user.is_authenticated:
        messages = Message.objects. \
            filter(recipient=request.user). \
            filter(status=Message.ST_WAITNG)
        messages_task = Message.objects. \
            filter(recipient=request.user). \
            filter(status=Message.ST_WAITNG, task=not None)
        messages_feedback = Message.objects. \
            filter(recipient=request.user). \
            filter(status=Message.ST_WAITNG, feedback=not None)
        messages_requests = Message.objects. \
            filter(recipient=request.user). \
            filter(status=Message.ST_WAITNG, requests=not None)
        return {'messages_for_user': messages,
                'messages_task': messages_task,
                'messages_feedback': messages_feedback,
                'messages_requests': messages_requests}
    return {}
