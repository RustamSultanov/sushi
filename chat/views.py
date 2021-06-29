from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
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
            context['chat_room_companion'] = chat_room.users.all().exclude(pk=self.request.user.id).first()
        if 'group' in self.request.GET:
            chat_room = Room.objects.get(pk=self.request.GET['group'])
            group_members = chat_room.users.all().exclude(pk=self.request.user.id)
            context['group_members'] = group_members

        context['chat_room'] = chat_room
        context['chat_messages'] = ChatMessage.objects.filter(room=chat_room)
        context['new_messages'] = ChatMessage.objects.filter(room=chat_room).filter(status='new')

        for msg in context['new_messages']: msg.change_status()
        return context


def new_group(request):
    members = User.objects.filter(pk__in=request.POST.getlist('users'))
    new_room = Room()
    new_room.name = request.POST.get("title", "groups")
    new_room.save()
    new_room.users.add(*members)
    new_room.users.add(request.user)
    return HttpResponseRedirect(f'/chat_page/?group={new_room.id}')

def update_group(request):
    members = User.objects.filter(pk__in=request.POST.getlist('users'))
    id_room = request.POST.get("room_id")
    new_room = Room.objects.get(pk = id_room)
    new_room.name = request.POST.get("title", "groups")
    new_room.save()
    new_room.users.add(*members)
    new_room.users.add(request.user)
    return HttpResponseRedirect(f'/chat_page/?group={new_room.id}')


def dell_group(request):
    try:
        member = User.objects.get(pk=request.GET.get('user'))
        room:Room = Room.objects.get(pk=request.GET.get('room_id'))
        room.users.remove(member)
        room.save()
    except ValueError:
        return HttpResponse('fail')

    return HttpResponseRedirect(f'/chat_page/?group={room.pk}')


@require_POST
def close_message(request):
    if 'message_id' in request.POST:
        try:
            message = ChatMessage.objects.get(pk=request.POST['message_id'])
        except ObjectDoesNotExist:
            return JsonResponse(status=404, data={"message": "Message not found"})
        else:
            message.status =ChatMessage.ST_READING
            message.save()
            return JsonResponse(status=200, data={"message": "Message reading"})
