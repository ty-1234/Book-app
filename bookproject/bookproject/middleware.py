# middleware.py

import socket
from django.contrib.sessions.models import Session
from django.utils import timezone

class SessionCleanupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not self.server_is_running():
            self.cleanup_sessions()
        return response

    def server_is_running(self):
        try:
            socket.create_connection(("127.0.0.1", 8000))  # Change to your server IP and port
            return True
        except OSError:
            return False

    def cleanup_sessions(self):
        now = timezone.now()
        expired_sessions = Session.objects.filter(expire_date__lt=now)
        expired_sessions.delete()
