
import os
import socket
import asyncio
import base64
import hashlib
import re
from urllib.parse import urlparse, parse_qs, unquote
from asyncio import StreamReader, StreamWriter




class WSGIServer:
    def __init__(self, host, port): self.host, self.port = host, port
    def serve_forever(self):
        sock=socket.socket(); sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        sock.bind((self.host,self.port)); sock.listen(5)
        print(f"WSGI on {self.host}:{self.port}")
        while True:
            conn,_=sock.accept(); self.handle(conn)
    def handle(self, conn):
        data=conn.recv(10**6)
        print(f"[WSGI]\n{data.decode(errors='ignore')}\n---")
        head,_,body=data.partition(b"\r\n\r\n")
        lines=head.decode().split("\r\n"); method,raw,_=lines[0].split(); parsed=urlparse(raw)
        hdrs=[(k.lower().encode(),v.encode()) for h in lines[1:] if ': ' in h for k,v in [h.split(': ',1)]]
        req=HttpRequest(method,parsed.path,parsed.query,hdrs,body)
        for pat,view in http_patterns:
            if (m:=pat.match(req.path.lstrip('/'))): req.kwargs=m.groupdict(); resp=view(req); break
        else: resp=HttpResponse('<h1>404</h1>',404)
        h,b=resp.to_bytes(); conn.sendall(h+b); conn.close()
