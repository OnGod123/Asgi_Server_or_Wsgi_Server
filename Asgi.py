import os
import socket
import asyncio
import base64
import hashlib
import re
from urllib.parse import urlparse, parse_qs, unquote
from asyncio import StreamReader, StreamWriter


class ASGIServer:
    def __init__(self, host, port): self.host, self.port=host,port
    def serve_forever(self): print(f"ASGI on {self.host}:{self.port}"); asyncio.run(self._run())
    async def _run(self): server=await asyncio.start_server(self.handle,self.host,self.port)
        async with server: await server.serve_forever()
    async def handle(self, reader:StreamReader, writer:StreamWriter):
        data=await reader.read(10**6)
        print(f"[ASGI HTTP]\n{data.decode('latin-1',errors='ignore')}\n---")
        head,_,body=data.partition(b"\r\n\r\n")
        lines=head.decode('latin-1').split("\r\n"); first=lines[0]
        hdrs=[(k.lower().encode(),v.encode()) for h in lines[1:] if ': ' in h for k,v in [h.split(': ',1)]]
        method,raw,_=first.split(); parsed=urlparse(raw)
        if any(k==b'upgrade' and b'websocket' in v.lower() for k,v in hdrs):
            path=parsed.path.rstrip('/'); Consumer=ws_patterns.get(path)
            if Consumer:
                scope={'type':'websocket','path':parsed.path,'headers':hdrs,'writer':writer,'reader':reader}
                await Consumer()(scope,None,None)
            writer.close(); return
        req=HttpRequest(method,parsed.path,parsed.query,hdrs,body)
        for pat,view in http_patterns:
            if (m:=pat.match(req.path.lstrip('/'))): req.kwargs=m.groupdict(); resp=await view(req) if asyncio.iscoroutinefunction(view) else view(req); break
        else: resp=HttpResponse('<h1>404</h1>',404)
        h,b=resp.to_bytes(); writer.write(h+b); await writer.drain(); writer.close()

