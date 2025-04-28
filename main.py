if __name__=='__main__':
    proto=os.getenv('SERVER_PROTOCOL','wsgi').lower()
    if proto=='asgi_http': ASGIServer('127.0.0.1',8000).serve_forever()
    elif proto=='asgi_ws': ASGIServer('127.0.0.1',8000).serve_forever()
    else: WSGIServer('127.0.0.1',8000).serve_forever()
