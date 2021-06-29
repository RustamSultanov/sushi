from .models import Message, ChatMessage
from django.contrib.auth import get_user_model

def messages_for_user(request):
    if request.user.is_authenticated:
        messages = Message.objects.select_related(
            "sender", "recipient", "requests", "idea", "task", "feedback"
        ).filter(recipient=request.user). \
            filter(status=Message.ST_WAITNG).order_by('-created_at')
        # messages_requests = Message.objects.exclude(requests__isnull=True).filter(status=Message.ST_WAITNG,
        #                                                                           recipient=request.user).count
        # messages_idea = Message.objects.exclude(idea__isnull=True).filter(status=Message.ST_WAITNG,
        #                                                                   recipient=request.user).count
        # messages_task = Message.objects.exclude(task__isnull=True).filter(status=Message.ST_WAITNG,
        #                                                                   recipient=request.user).count
        # messages_feedback = Message.objects.exclude(feedback__isnull=True).filter(status=Message.ST_WAITNG,
        #                                                                           recipient=request.user).count
        room = request.user.room_set.all()
        users = get_user_model().objects.all().exclude(pk=request.user.id)
        messages_chat_groups = ChatMessage.objects.filter(room__in=room, ).filter(status='new').order_by('sent_time')
        messages_chat_user = ChatMessage.objects.filter(user_from__in=users).filter(status='new')
        messages_chat_user = messages_chat_user.difference(messages_chat_groups).order_by('sent_time')

        messages_chat: list[dict] = []

        for ch in messages_chat_groups:
            messages_chat.append(
            {   "id": ch.id,
                "url": f"/chat_page/?group={ ch.room.id }",
                "text": ch.text,
                "text_light": f"{ ch.room.name } · { ch.sent_time.strftime('%Y-%m-%d %H:%M:%S') }",
            }
        )
        for ch in messages_chat_user:
            messages_chat.append(
            {   "id": ch.id,
                "url": f"/chat_page/?user={ ch.user_from }",
                "text": ch.text,
                "text_light": f"{ ch.user_from } .  { ch.sent_time.strftime('%Y-%m-%d %H:%M:%S') }",
            }
        )
        return {
                # 'messages_requests': messages_requests,
                # 'messages_idea': messages_idea,
                'messages_for_user': messages,
                # 'messages_task': messages_task,
                # 'messages_feedback': messages_feedback,
                "new_chat_message": {
                                        "count": messages_chat_user.count() + messages_chat_groups.count(),
                                        # "groups": messages_chat_groups,
                                        # "users": messages_chat_user,
                                        "message":sorted(messages_chat, key= lambda x: x["id"])
                                    },
        }
    return {}
