from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

from .exceptions import ClientError
from .models import Room


@database_sync_to_async
def get_room_or_error(room_id, user):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    # Check if the user is logged in
    if not user.is_authenticated:
        raise ClientError("USER_HAS_TO_LOGIN")
    # Find the room they requested (by ID)
    try:
        room = Room.objects.get_or_create(pk=room_id)
    except Room.DoesNotExist:
        raise ClientError("ROOM_INVALID")
    return room[0]

@database_sync_to_async
def get_user_or_error(user:int):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """

    try:
        user = get_user_model().objects.get_or_create(pk=user)
    except get_user_model().DoesNotExist:
        raise ClientError("ROOM_INVALID")

    return user[0]
