import asyncio
import json
import threading
import traceback

import websockets
from websockets.legacy.server import serve as websockets_serve

lock = threading.Lock()


class Websocket_connection():
    def __init__(self, port=7306):
        self.messages_sent = 0
        self.overlay_messages = []
        self.port = port

    def run(self):
        try:
            print('Starting websocket server')
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            start_server = websockets_serve(self.manager, 'localhost',
                                            self.port)
            loop.run_until_complete(start_server)
            loop.run_forever()
        except Exception:
            traceback.print_exc()

    async def manager(self, websocket, path):
        """ Manages websocket connection for each client """
        print(f"Opening: {websocket}")

        # Send the last message if there is one
        if len(self.overlay_messages) > 0:
            self.send(self.overlay_messages[-1]) 
        sent = self.messages_sent

        while True:
            try:
                if len(self.overlay_messages) == sent:
                    continue

                message = json.dumps(self.overlay_messages[sent])
                print(f"WS sending: {self.overlay_messages[sent]}")
                sent += 1
                await asyncio.wait_for(asyncio.gather(websocket.send(message)),
                                       timeout=1)
            except asyncio.TimeoutError:
                print(f'#{sent-1} message was timed-out.')

            except websockets.exceptions.ConnectionClosedOK:
                print('Websocket connection closed (ok).')
                break

            except websockets.exceptions.ConnectionClosedError:
                print('Websocket connection closed (error).')
                break

            except websockets.exceptions.ConnectionClosed:
                print('Websocket connection closed.')
                break

            except Exception:
                traceback.print_exc()

            finally:
                await asyncio.sleep(0.1)

    def send(self, event):
        """ Send message throught a websocket """
        with lock:
            self.messages_sent += 1
            self.overlay_messages.append(event)
