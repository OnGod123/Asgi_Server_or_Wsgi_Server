import os
import socket
import asyncio
import base64
import hashlib
import re
from urllib.parse import urlparse, parse_qs, unquote
from asyncio import StreamReader, StreamWriter


class HttpRequest:
    def __init__(self, method, path, query_string, headers, body, kwargs=None):
        self.method = method.upper()
        self.path = path
        self.GET = parse_qs(query_string)
        self.POST = {}
        self.FILES = {}
        self.headers = {k.decode(): v.decode() for k, v in headers}
        self.body = body
        self.kwargs = kwargs or {}
        if self.method == 'POST':
            ctype = self.headers.get('Content-Type', '')
            if 'application/x-www-form-urlencoded' in ctype:
                self.POST = parse_qs(body.decode())
            elif 'multipart/form-data' in ctype:
                boundary = ctype.split('boundary=')[-1]
                self._parse_multipart(body, boundary)

    def _parse_multipart(self, data, boundary):
        parts = data.split(b'--' + boundary.encode())
        for part in parts:
            if not part or part.startswith(b'--\r\n'): continue
            head, _, value = part.partition(b'\r\n\r\n')
            headers = head.decode().split("\r\n")
            disp = next(h for h in headers if h.startswith('Content-Disposition'))
            name = re.search(r'name="(\w+)"', disp).group(1)
            filename_match = re.search(r'filename="(.+?)"', disp)
            if filename_match:
                filename = filename_match.group(1)
                self.FILES[name] = {'filename': filename, 'content': value.rstrip(b"\r\n")}
            else:
                self.POST[name] = value.decode().rstrip('\r\n')
