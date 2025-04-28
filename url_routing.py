http_patterns = []
ws_patterns = {}

def path(route, view):
    pattern = '^' + re.sub(r'<str:(\w+)>', r'(?P<\1>[^/]+)', route.rstrip('/')) + '/?$'
    http_patterns.append((re.compile(pattern), view))

def ws_path(route, consumer_cls):
    ws_patterns[route.rstrip('/')] = consumer_cls

