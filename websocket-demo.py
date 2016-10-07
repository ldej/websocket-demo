import asyncio

from aiohttp import WSMsgType
from aiohttp import web


class WebSocket:
    websockets = []
    request = None

    async def get(self, request):
        self.request = request
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        for _ws in self.websockets:
            _ws.send_str('Someone joined')
        self.websockets.append(ws)

        async for msg in ws:
            if msg.tp == WSMsgType.text:
                if msg.data == 'close':
                    await ws.close()
                else:
                    for _ws in self.websockets:
                        _ws.send_str(msg.data)
            elif msg.tp == WSMsgType.error:
                ws.exception()

        self.websockets.remove(ws)
        for _ws in self.websockets:
            _ws.send_str('Someone disconnected')

        return ws


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    app = web.Application(loop=loop)
    handler = WebSocket()
    app.router.add_get('/websocket', handler.get)
    web.run_app(app)
