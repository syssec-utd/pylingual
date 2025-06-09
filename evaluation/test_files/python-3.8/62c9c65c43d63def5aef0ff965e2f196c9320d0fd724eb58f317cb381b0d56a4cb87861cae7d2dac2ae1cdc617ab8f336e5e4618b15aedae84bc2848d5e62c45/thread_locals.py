import threading
_thread_locals = threading.local()

def get_current_request():
    return getattr(_thread_locals, 'request', None)

def set_current_request(request):
    _thread_locals.request = request