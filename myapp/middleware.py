import logging
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from django.contrib.auth.models import AnonymousUser

logger = logging.getLogger(__name__)

class UserActivityLoggingMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if isinstance(request.user, AnonymousUser):
            user_id = 'anonymous'
        else:
            user_id = request.user.id

        path = request.path
        cache_key = f'user_activity_{user_id}'
        activity_log = cache.get(cache_key, [])

        activity_entry = {'path': path, 'method': request.method}
        activity_log.append(activity_entry)

        try:
            cache.set(cache_key, activity_log, timeout=60)  # Хранение логов в течение 60 sec
            logger.info(f"Cache set for key {cache_key}")
        except Exception as e:
            logger.error(f"Error setting cache for key {cache_key}: {e}")

        logger.info(f"User {user_id} visited {path} with method {request.method}")
