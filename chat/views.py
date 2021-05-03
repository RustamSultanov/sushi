from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.generic.base import TemplateView
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q

from .models import ChatMessage, Room


User = get_user_model()

class ChatPage(TemplateView):
    template_name = 'chat/chat.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rooms'] = Room.objects.filter(users=self.request.user)
        rooms = Room.objects.filter(users=self.request.user)
        context['users'] = User.objects.all().exclude(pk=self.request.user.id)
        chat_room = None
        # if rooms:
        #     chat_room = rooms[0]
        if 'with_user' in self.request.GET:
            with_user = User.objects.get(pk=self.request.GET['with_user'])
            chat_room = rooms.filter(users=self.request.user).filter(users=with_user).first()
            if not chat_room:
                # users = User.objects.filter(Q(pk=self.request.user.id) |          Q(pk=with_user.id))
                users = [self.request.user, with_user]
                chat_room = Room()
                chat_room.save()
                chat_room.users.add(*users)
            print(chat_room)
        context['chat_room'] = chat_room
        context['chat_messages'] = ChatMessage.objects.filter(room=chat_room)
        if chat_room:
            context['chat_room_companion'] = chat_room.users.all().exclude(pk=self.request.user.id).first()
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
