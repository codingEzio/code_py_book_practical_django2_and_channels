from django.urls import re_path

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.http import AsgiHandler

from main import routing as appmain_routing

__doc__ = """ A little bit explanation about stuff inside `application`.

[ProtocolTypeRouter]
    We need to separate 'WebSocket-handling' code from normal 'views'.
    And , we'll use "routers" together with special middleware (<= channels).

[AuthMiddlewareStack]
    This "middleware" is NOT the same as the one in Django (x.x.csrf.CsrfViewMiddleware).
    This one is FULLY asynchronous
        and offering similar features like <filtering>, <blocking>
        and adding   additional info  to   <scopes> (an object used in 'consumers.py')

And one more thing
    If a http argument is not provided,
    it will default to the Django view system’s ASGI interface (`channels.http.AsgiHandler`), 
    
    which means that 
        for most projects that aren’t doing custom long-poll HTTP handling, 
        you can simply not specify a http option & leave it to work “normal” Django way.

#TODO NEW EXPLANATION NEEDED
"""

application = ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(
            URLRouter(
                appmain_routing.websocket_urlpatterns
            )
        ),
        "http": URLRouter(
            appmain_routing.http_urlpatterns \
            + [
                re_path(r"", AsgiHandler)
            ]
        )
    }
)
