import json, logging, datetime, os, logging, base64
from aiohttp import web, ClientSession, WSMsgType
from django.apps import apps
from django.conf import settings
from django.contrib.auth import authenticate, login
from channels.db import database_sync_to_async
from django.conf import settings
from django.core.files.base import ContentFile

logging.basicConfig(filename="task_book.log", level=logging.INFO)

class MixView():

    def get_m(self, model_name):
        model_obj = apps.get_model(model_name)
        return model_obj

    @database_sync_to_async
    def new_mes(self, text, room, user_id, file, filename=None):
        User = self.get_m(settings.AUTH_USER_MODEL)
        Room = self.get_m('chat.Room')
        ChatMessage = self.get_m('chat.ChatMessage')
        mes = ChatMessage(
            user_from=User.objects.get(pk=user_id),
            room=Room.objects.get(pk=room),
            text=text,
            # file=file,
        )
        mes.save()
        if file:
            head, data = file.split(',')
            # decoded =data.decode('base64','strict');
            # print(head)
            print(filename)
            fl = ContentFile(base64.b64decode(data), name=filename)
            mes.file = fl
            mes.save()
        return mes



class WSChat(web.View, MixView):

    async def get(self):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        async for msg in ws:
            # print(self.request.app.wslist) views

            if msg.type == WSMsgType.BINARY:
                print(msg.extra)
            else:
                mes_dict = json.loads(msg.data)
                # print(mes_dict)
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
        for us, peer in self.request.app.wslist[mes.room.id].items():
            try:
                avatar = None
                # if mes.from_user.avatar:
                #     avatar = mes.from_user.avatar.url
                text = mes.text
                if mes.file:
                    text = f'{mes.text} приложено: <a href="/media/{mes.file.url}">{mes.file.url}</a>'
                    print(text)
                await peer.send_json({
                'text':text,
                'from_name': mes.user_from.username,
                'time': mes.sent_time.strftime("%d.%m.%Y, %H:%M:%S"),
                'avatar': avatar
                })
            except Exception as e:
                # print(e)
                await peer.close()
                pass
