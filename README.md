Core Python WSGI/ASGI Switch Server

This repository contains a minimal core Python server that simulates Django’s WSGI and ASGI servers:

WSGI HTTP (synchronous HTTP GET/POST, including file uploads)

ASGI HTTP (asynchronous HTTP handling)

ASGI WebSocket (full-duplex WebSocket support via HTTP upgrade)

All in a single server.py script, switchable via the SERVER_PROTOCOL environment variable.

Features

URL Routing: Register routes with path("route/", view_func) similar to Django.

HTTP Methods:

GET & POST

Form data (application/x-www-form-urlencoded)

File uploads (multipart/form-data)

Template Rendering: Simple render(template_name, context) loading HTML from ./templates/.

WebSocket Support:

Performs the HTTP Upgrade handshake.

Parses incoming frames (text & binary).

Echo and file-upload WebSocket consumers as examples.

Server Modes:

wsgi (default): Synchronous, one-request-at-a-time.

asgi_http: Asynchronous HTTP server.

asgi_ws: Asynchronous WebSocket server.

Logging: Prints raw HTTP requests and WebSocket handshake/frames to the console.

Getting Started

Clone this repository:

git clone <repo-url>
cd <repo-dir>

Create a templates/ directory and add home.html, upload.html, etc.

Run the server:

# WSGI HTTP (synchronous)
python server.py

# ASGI HTTP (asynchronous HTTP)
SERVER_PROTOCOL=asgi_http python server.py

# ASGI WebSocket (real-time)
SERVER_PROTOCOL=asgi_ws python server.py

Visit in your browser or curl:

HTTP:  http://127.0.0.1:8000/

Trends: http://127.0.0.1:8000/trends/

Upload form: http://127.0.0.1:8000/upload/

WebSocket (in JS):

const ws = new WebSocket('ws://127.0.0.1:8000/ws/echo/');
ws.onmessage = e => console.log('Received:', e.data);
ws.onopen = () => ws.send('Hello');

Code Overview

HttpRequest/HttpResponse: Classes modeling HTTP request/response.

render(): Loads templates from templates/ and formats with context.

Routing:

path(route, view) for HTTP views.

ws_path(route, consumer_cls) for WebSocket consumers.

WebSocketConsumer: Base class handling handshake, frame parsing, and send/receive.

reader_read_frame: Parses WebSocket frames (opcode, length, mask, payload).

WSGIServer: Synchronous socket loop for HTTP only.

ASGIServer: Asyncio-based server supporting both HTTP and WebSocket upgrade.

Extending

Add new URL patterns via path.

Implement new WebSocket consumers inheriting from WebSocketConsumer.

Enhance template engine or static file serving.

Plug in real Django apps by embedding django.core.wsgi or django.core.asgi apps.

License

MIT © Vincent ifejika


