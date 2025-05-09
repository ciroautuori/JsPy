from starlette.types import Scope, Receive, Send, ASGIApp

class HttpsRedirectFixMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        # Forza lo scheme su https se arriva da reverse proxy
        if scope["type"] == "http" and scope.get("headers"):
            headers = dict(scope["headers"])
            x_proto = headers.get(b"x-forwarded-proto", b"").decode()
            if x_proto == "https":
                scope["scheme"] = "https"
        await self.app(scope, receive, send)
