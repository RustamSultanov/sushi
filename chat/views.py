from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.generic.base import TemplateView
from django.conf import settings


from .models import Message, Room


class ChatPage(TemplateView):
    template_name = 'chat/chat.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rooms'] = Room.objects.filter(users=request.user)
        rooms = Room.objects.filter(users=request.user)
        context['users'] = settings.AUTH_USER_MODEL.objects.all()
        chat_room = rooms[]
        if rooms:
            if 'room' ib request.GET:
                chat_room = rooms.get(pk=request.GET['room])
            context['chat_room'] = chat_room
            context['chat_messages'] = Message.objects.filter(room=chat_room)
            context['chat_room_companion'] = chat_room.users.all().exclude(pk=request.user.id).first()
        return context


@require_POST
def close_message(request):
    if 'message_id' in request.POST:
        try:
            message = Message.objects.get(pk=request.POST['message_id'])
        except ObjectDoesNotExist:
            return JsonResponse(status=404, data={"message": "Message not found"})
        else:
            message.status =Message.ST_READING
            message.save()
            return JsonResponse(status=200, data={"message": "Message reading"})
