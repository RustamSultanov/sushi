import aioreloader
from aiohttp import web
from django import setup
from django.conf import settings
import os
from my_proj import settings as my_settings
from chat import aioviews


async def setup_django(app):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'my_proj.settings'
    settings.configure(
        INSTALLED_APPS=my_settings.INSTALLED_APPS,
        DATABASES=my_settings.DATABASES
    )
    setup()

aioreloader.start()

async def app_factory():
    app = web.Application()
    # app.add_routes([web.get('/', aioviews.index)])
    app.on_startup.append(setup_django)
    app.router.add_route('*', '/ws/chat/', aioviews.WSChat)
    # app.add_subapp('/aio/', index)
    app.wslist = {}

    return app

if __name__ == '__main__':
    web.run_app(app_factory())
