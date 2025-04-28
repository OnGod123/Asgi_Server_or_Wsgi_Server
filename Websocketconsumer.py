import os
import socket
import asyncio
import base64
import hashlib
import re
from urllib.parse import urlparse, parse_qs, unquote
from asyncio import StreamReader, StreamWriter


class WebSocketConsumer:
    async def __call__(self, scope, receive, send):
        print(f"[WSS] Handshake headers: {scope['headers']}")
        headers = {k.decode().lower(): v.decode() for k,v in scope['headers']}
        key = headers['sec-websocket-key']
        accept = base64.b64encode(hashlib.sha1((key + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11').encode()).digest()).decode()
        response = ("HTTP/1.1 101 Switching Protocols\r\n"
                    "Upgrade: websocket\r\n"
                    "Connection: Upgrade\r\n"
                    f"Sec-WebSocket-Accept: {accept}\r\n\r\n").encode()
        # Extract the StreamWriter from scope, with a type hint for clarity
        writer: StreamWriter = scope['writer']  # 'writer' is an asyncio StreamWriter used to send bytes back to the client
        writer.write(response)
        await writer.drain()
        print("[WSS] Handshake sent")
        reader: StreamReader = scope['reader']
        while True:
            frame = await reader_read_frame(reader)
            if not frame: break
            print(f"[WSS] Frame: {frame}")
            if frame['type']=='text': await self.receive(frame['data'], scope)
            else: await self.receive_binary(frame['data'], scope)
        print("[WSS] Closed")

    async def receive(self, text_data, scope): pass
    async def receive_binary(self, data, scope): pass
    async def disconnect(self, scope): pass

class EchoConsumer(WebSocketConsumer):
    async def receive(self, text_data, scope):
        writer: StreamWriter = scope['writer']; msg = text_data.encode();
        writer.write(b'\x81' + bytes([len(msg)]) + msg); await writer.drain()
    async def receive_binary(self, data, scope):
        writer: StreamWriter = scope['writer']; writer.write(b'\x82' + bytes([len(data)]) + data); await writer.drain()

