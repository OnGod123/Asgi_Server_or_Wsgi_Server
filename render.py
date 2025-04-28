import os
import socket
import asyncio
import base64
import hashlib
import re
from urllib.parse import urlparse, parse_qs, unquote
from asyncio import StreamReader, StreamWriter

def render(template_name, context=None, status=200):
    try:
        text = open(os.path.join('templates', template_name), encoding='utf8').read()
    except FileNotFoundError:
        return HttpResponse('<h1>Template not found</h1>', status=404)
    if context:
        text = text.format(**context)
    return HttpResponse(text, status=status)

