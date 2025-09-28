import os
from django.conf import settings
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

class RequestLoggingMiddleware:
    """
    Middleware that logs each user’s request with timestamp, user and path.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.log_path = os.path.join(settings.BASE_DIR, "requests.log")

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_line = f"{datetime.now()} - User: {user} - Path: {request.path}\n"
        with open("requests.log", "a") as log_file:
            log_file.write(log_line)
        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    """
    Middleware that restricts access outside the allowed hours: 6 AM to 9 PM.
    Returns HTTP 403 Forbidden if accessed outside the allowed time window.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.start_hour = 6
        self.end_hour = 21

    def __call__(self, request):
        current_hour = datetime.now().hour
        if current_hour < self.start_hour or current_hour >= self.end_hour:
            return JsonResponse({"detail": "Access restricted during this time."}, status=403)
        return self.get_response(request)


class OffensiveLanguageMiddleware:
    """
    Middleware that limits the number of POST requests (messages) per IP address
    to 5 messages per minute.
    Blocks the user with HTTP 429 Too Many Requests if the limit is exceeded.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_message_counts = {}  # Store {ip: [(timestamp1), (timestamp2), ...]}
        self.time_window = timedelta(minutes=1)
        self.limit = 5

    def __call__(self, request):
        if request.method == "POST":
            ip = self.get_client_ip(request)
            now = datetime.now()
            timestamps = self.ip_message_counts.get(ip, [])
            # Remove timestamps older than time window
            timestamps = [ts for ts in timestamps if now - ts < self.time_window]
            if len(timestamps) >= self.limit:
                return JsonResponse({"detail": "Message rate limit exceeded."}, status=429)
            timestamps.append(now)
            self.ip_message_counts[ip] = timestamps

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RolePermissionMiddleware:
    """
    Middleware that restricts access to users with 'admin' or 'moderator' roles.
    Returns HTTP 403 Forbidden for unauthorized users.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_roles = {'admin', 'moderator'}

    def __call__(self, request):
        user = request.user

        if user.is_authenticated:
            if getattr(user, 'role', None) not in self.allowed_roles:
                return JsonResponse({'detail': 'You do not have permission to perform this action.'}, status=403)
        else:
            return JsonResponse({'detail': 'Authentication credentials were not provided.'}, status=401)

        return self.get_response(request)
