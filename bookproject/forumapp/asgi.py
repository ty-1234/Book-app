import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import forumapp.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookproject.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            forumapp.routing.websocket_urlpatterns
        )
    ),
})
