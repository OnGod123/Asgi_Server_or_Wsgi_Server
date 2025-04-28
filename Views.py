def home_view(request): return render('home.html', {'path': request.path})
def trends_view(request): return HttpResponse('<h2>All Trends</h2>')
def trend_detail(request): return HttpResponse(f'<h2>Trend: {unquote(request.kwargs.get("trend",""))}</h2>')
def upload_form(request): return render('upload.html')
def upload_view(request):
    file_info = request.FILES.get('file')
    if not file_info: return HttpResponse('<h1>No file</h1>', status=400)
    os.makedirs('uploads', exist_ok=True)
    with open(os.path.join('uploads', file_info['filename']), 'wb') as f: f.write(file_info['content'])
    return HttpResponse(f'<h1>Saved {file_info["filename"]}</h1>')
async def asgi_http_view(request): return HttpResponse(f'<p>[ASGI] {request.method} at {request.path}</p>')

path('', home_view)
path('trends/', trends_view)
path('trends/<str:trend>/', trend_detail)
path('upload/', upload_form)
path('upload/', upload_view)

