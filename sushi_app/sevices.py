from django.conf import settings
from django.core.exceptions import PermissionDenied

User = settings.AUTH_USER_MODEL


class PartnerService:

    @staticmethod
    def delete_partner(user, partner_user):
        if not user.user_profile.user_is_manager:
            raise PermissionDenied
        partner_profile = partner_user.user_profile

        if not partner_profile or not partner_profile.is_partner:
            raise PermissionDenied

        if not user.user_profile.is_head:
            if partner_profile.manager != user.user_profile:
                raise PermissionDenied
        partner_profile.user.delete()


class ShopService:
    @staticmethod
    def delete_shop(user, shop):
        if not (user.user_profile.user_is_manager or shop.partner.id == user.user_profile.id):
            raise PermissionDenied
        shop.delete()
