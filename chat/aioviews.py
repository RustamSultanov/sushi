import ujson, json, logging, datetime, os
from aiohttp import web, ClientSession, WSMsgType
from django.apps import apps
from django.conf import settings
from django.contrib.auth import authenticate, login
from channels.db import database_sync_to_async


class MixView():

    def get_m(self, model_name):
        model_obj = apps.get_model(model_name)
        return model_obj

    @database_sync_to_async
    def new_mes(self, text, room, user_id, file, filename=None):
        Person = self.get_m('Manage.Person')
        ChatRoom = self.get_m('Mess.ChatRoom')
        ChatMessage = self.get_m('Mess.ChatMessage')
        mes = ChatMessage(
            user=Person.objects.get(pk=user_id),
            room=ChatRoom.objects.get(pk=room),
            text=text,
            # file=file,
        )
        mes.save()
        if file:
            head, data = file.split(',')
            # decoded =data.decode('base64','strict');
            print(head)
            fl = ContentFile(base64.b64decode(data), name=f'{mes.id}_{filename}')
            mes.file = fl
            mes.save()
        return mes



class WebSocket(web.View, MixView):

    async def get(self):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        async for msg in ws:
            # print(self.request.app.wslist) views

            if msg.type == WSMsgType.BINARY:
                print(msg.extra)
            else:
                mes_dict = json.loads(msg.data)
                print(mes_dict)
                if mes_dict['text'] or mes_dict['file']:

                    mes = await self.new_mes(
                        mes_dict['text'],
                        mes_dict['room'],
                        mes_dict['user_id'],
                        mes_dict['file'],
                        mes_dict['filename']
                    )
                    await self.broadcast(mes)
                if mes_dict['room'] not in self.request.app.wslist:
                    self.request.app.wslist[mes_dict['room']] = {}
                self.request.app.wslist[mes_dict['room']][mes_dict['user_id']] = ws


    async def broadcast(self, mes):
        """ Send messages to all in this room
        # TODO: реализовать историю с прочитанными/непрочитанными сообщениями и с
        уведомлением о непрочитанных сообщениях при подключении пира
         """
        for us, peer in self.request.app.wslist[room].items():
            try:
                avatar = None
                if mes.from_user.avatar:
                    avatar = mes.from_user.avatar.url
                await peer.send_json({
                'text':mes.text,
                'from_name': mes.user_from.username,
                'time': mes.sent_time.strftime("%d.%m.%Y, %H:%M:%S"),
                'avatar': avatar
                })
            except Exception as e:
                # print(e)
                await peer.close()
                pass
