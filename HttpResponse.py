import os
import socket
import asyncio
import base64
import hashlib
import re
from urllib.parse import urlparse, parse_qs, unquote
from asyncio import StreamReader, StreamWriter

class HttpResponse:
    STATUS_TEXT = {200: 'OK', 404: 'Not Found'}
    def __init__(self, content, status=200, headers=None):
        self.status = status
        self.content = content if isinstance(content, bytes) else content.encode()
        self.headers = headers.copy() if headers else {}
        self.headers.setdefault('Content-Type', 'text/html')
        self.headers['Content-Length'] = str(len(self.content))
    def to_bytes(self):
        status_line = f"HTTP/1.1 {self.status} {HttpResponse.STATUS_TEXT[self.status]}\r\n"
        hdrs = ''.join(f"{k}: {v}\r\n" for k, v in self.headers.items())
        return (status_line + hdrs + "\r\n").encode(), self.content
