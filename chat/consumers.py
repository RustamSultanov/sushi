from base64 import b64decode

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.core.files.base import ContentFile

from .exceptions import ClientError
from .models import ChatMessage , ChatMessageFile
from .utils import get_room_or_error


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        """
        Called when the websocket is handshaking as part of initial connection.
        """
        # Are they logged in?
        if self.scope["user"].is_anonymous:
            # Reject the connection
            await self.close()
        else:
            # Accept the connection
            await self.accept()
        # Store which rooms the user has joined on this connection
        self.rooms = set()

    async def disconnect(self, code):
        """
        Called when the WebSocket closes for any reason.
        """

        # Leave all the rooms we are still in
        for room_id in list(self.rooms):
            try:
                await self.leave_room(room_id)
            except ClientError:
                pass

    async def receive_json(self, content: dict):
        """
        Called when we get a text frame. Channels will JSON-decode the payload
        for us and pass it as the first argument.
        """
        # Messages will have a "command" key we can switch on
        # content == {'text': '', 'room': 3, 'user_id': 4, 'file': None, 'filename': None}

        if not content['room'] in self.rooms:
            await self.join_room(content['room'])

        if content['filename']:
            meta, img_str = content['file'].split(';base64,')
            cf = ContentFile(name=content['filename'], content=b64decode(img_str))
            file = ChatMessageFile(
                name=content['filename'],
                file = cf
            )
            file.save()
        else:
            file = None
        if content['text'] != '' or file != None:
            ins = ChatMessage()
            ins.user_from_id = content['user_id']
            ins.room_id = content['room']
            ins.text = content['text']
            ins.file = file

            async_to_sync(ins.save())
            await self.send_room(content['room'], ins)

    async def join_room(self, room_id):
        """
        Called by receive_json when someone sent a join command.
        """
        # The logged-in user is in our scope thanks to the authentication ASGI middleware
        room = await get_room_or_error(room_id, self.scope["user"])
        # Send a join message if it's turned on

        # await self.channel_layer.group_send(
        #         room.group_name,
        #         {
        #             "type": "chat.join",
        #             "room_id": room_id,
        #             "username": self.scope["user"].username,
        #         }
        #     )
        # Store that we're in the room
        self.rooms.add(room_id)

        # Add them to the group so they get room messages
        await self.channel_layer.group_add(
            room.group_name,
            self.channel_name,
        )

        # Instruct their client to finish opening the room
        # await self.send_json({
        #     "join": str(room.id),
        #     "title": room.group_name,
        # })

    async def leave_room(self, room_id):
        """
        Called by receive_json when someone sent a leave command.
        """
        # The logged-in user is in our scope thanks to the authentication ASGI middleware
        room = await get_room_or_error(room_id, self.scope["user"])
        # Send a leave message if it's turned on
        await self.channel_layer.group_send(
            room.group_name,
            {
                "type": "chat.leave",
                "room_id": room_id,
                "username": self.scope["user"].username,
            }
        )
        # Remove that we're in the room
        self.rooms.discard(room_id)
        # Remove them from the group so they no longer get room messages
        await self.channel_layer.group_discard(
            room.group_name,
            self.channel_name,
        )
        # Instruct their client to finish closing the room
        await self.send_json({
            "leave": str(room.id),
        })

    async def send_room(self, room_id, message: ChatMessage):
        """
        Called by receive_json when someone sends a message to a room.
        """
        # Check they are in this room
        if room_id not in self.rooms:
            raise ClientError("ROOM_ACCESS_DENIED")
        # Get the room and send to the group about it
        room = await get_room_or_error(room_id, self.scope["user"])
        try:
            avatar = self.scope["user"].avatar.url
        except AttributeError:
            avatar = '/'
        obj = {
            "type": "chat.message",
            "room_id": room_id,
            "from_name": message.user_from.username,
            "avatar": avatar,
            "time": message.sent_time.strftime('%d.%m.%Y %H:%M'),
            "text": message.text,
        }
        if message.file:
            obj["file"] = message.file.name,
            obj["file_url"] = message.file.file.url
        await self.channel_layer.group_send(
            room.group_name, obj
        )

    ##### Handlers for messages sent over the channel layer

    # These helper methods are named by the types we send - so chat.join becomes chat_join
    async def chat_join(self, event):
        """
        Called when someone has joined our chat.
        """
        # Send a message down to the client
        await self.send_json(
            {
                "msg_type": 'ENTER',
                "room": event["room_id"],
                "username": event["username"],
            },
        )

    async def chat_leave(self, event):
        """
        Called when someone has left our chat.
        """
        # Send a message down to the client
        await self.send_json(
            {
                "msg_type": 'LEAVE',
                "room": event["room_id"],
                "username": event["username"],
            },
        )

    async def chat_message(self, event: dict):
        """
        Called when someone has messaged our chat.
        """
        # Send a message down to the client
        # {'type': 'chat.message', 'room_id': '6', 'from_name': 'franch1', 'avatar': '/', 'text': 'test'}
        data = {
            "msg_type": 'MESSAGE',
            "room": event["room_id"],
            "time": event['time'],
            "text": event["text"],
        }
        if event.get("file"):
            data["file"] = event["file"],
            data["file_url"] = event["file_url"]

        if event['avatar'] != '/':
            data["avatar"] = event['avatar']
        if event['from_name'] == self.scope['user'].username:
            data["from_name"] = "You"
        else:
            data["from_name"] = event['from_name']
        await self.send_json(data, )
