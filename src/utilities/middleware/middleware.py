try:
    from threading import local, current_thread
except ImportError:
    from django.utils._threading_local import local

_thread_locals = local()

from django.contrib.sessions.models import Session
from django.utils.timezone import now
from django.core.cache import cache
from src.modules.tools.models import SiteStatistics


class GlobalUserMiddleware(object):
    """
    Sets the current authenticated user in threading locals

    Usage example:
        from app_name.middleware import get_current_user
        user = get_current_user()
    """

    def process_request(self, request):
        setattr(
            _thread_locals,
            'user_{0}'.format(current_thread().name),
            request.user)

    def process_response(self, request, response):
        key = 'user_{0}'.format(current_thread().name)

        if not hasattr(_thread_locals, key):
            return response

        delattr(_thread_locals, key)

        return response


def get_current_user():
    return getattr(
        _thread_locals,
        'user_{0}'.format(current_thread().name),
        None
    )

# class CountVisitsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Tạo session nếu chưa tồn tại
        if not request.session.session_key:
            request.session.create()

        # Đếm số người online (dựa vào session chưa hết hạn)
        online_count = Session.objects.filter(expire_date__gte=now()).count()

        # Kiểm tra và cập nhật tổng lượng truy cập (nếu là session mới)
        session_key = f"visited_{request.session.session_key}"
        if not cache.get(session_key):  # Nếu session chưa được ghi nhận
            SiteStatistics.increment_visits()  # Tăng tổng lượt truy cập
            cache.set(session_key, True, timeout=3600)  # Đánh dấu session này, timeout 1 giờ

        # Gắn số người online vào request để truy cập trong views
        request.online_count = online_count

        return self.get_response(request)
    
    
    
# class CountVisitsMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # Tạo session nếu chưa tồn tại
#         if not request.session.session_key:
#             request.session.create()

#         session_key = request.session.session_key
#         online_key = f"online_{session_key}"

#         # Kiểm tra và cập nhật số người online
#         if not cache.get(online_key):  # Nếu session chưa được ghi nhận là online
#             # Tăng số người online
#             self.increment_online_count()

#             # Đánh dấu session này là online với timeout 1 giờ
#             cache.set(online_key, True, timeout=300)  # Timeout 1 giờ

#         # Đếm số người online (dựa vào session chưa hết hạn)
#         online_count = self.get_online_count()

#         # Kiểm tra và cập nhật tổng lượng truy cập (nếu là session mới)
#         session_key_check = f"visited_{request.session.session_key}"
#         if not cache.get(session_key_check):  # Nếu session chưa được ghi nhận
#             SiteStatistics.increment_visits()  # Tăng tổng lượt truy cập
#             cache.set(session_key_check, True, timeout=300)  # Đánh dấu session này, timeout 1 giờ

#         # Gắn số người online vào request để truy cập trong views
#         request.online_count = online_count

#         return self.get_response(request)

#     def increment_online_count(self):
#         """ Tăng số người online """
#         current_online = cache.get('online_count', 0)
#         cache.set('online_count', current_online + 1)

#     def decrement_online_count(self):
#         """ Giảm số người online """
#         current_online = cache.get('online_count', 0)
#         if current_online > 0:
#             cache.set('online_count', current_online - 1)

#     def get_online_count(self):
#         """ Lấy số người online hiện tại từ cache """
#         return cache.get('online_count', 0)


# Callback giảm số người online khi session hết hạn
def session_expired(sender, instance, **kwargs):
    # Gọi giảm số người online khi session hết hạn
    session_key = instance.session_key
    online_key = f"online_{session_key}"

    # Tạo đối tượng CountVisitsMiddleware để gọi phương thức giảm số người online
    middleware = CountVisitsMiddleware(None)
    
    if cache.get(online_key):
        cache.delete(online_key)  # Xóa session online
        middleware.decrement_online_count()  # Giảm số người online
        
        
        
        
        
from datetime import datetime, timedelta
from django.core.cache import cache

class CountVisitsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Tạo session nếu chưa tồn tại
        if not request.session.session_key:
            request.session.create()

        session_key = request.session.session_key
        online_key = f"online_{session_key}"

        # Lưu danh sách các session online trong cache
        active_sessions_key = 'active_sessions'  # Lưu key danh sách các session online

        # Lấy danh sách session đang online từ cache
        active_sessions = cache.get(active_sessions_key, set())

        # Kiểm tra nếu session chưa có trong danh sách
        if online_key not in active_sessions:
            # Thêm session vào danh sách và cập nhật cache
            active_sessions.add(online_key)
            cache.set(active_sessions_key, active_sessions, timeout=3600)  # Timeout 1 giờ

            # Tăng số người online
            self.increment_online_count()

        # Cập nhật thời gian last active của session này
        cache.set(online_key, datetime.now(), timeout=3600)

        # Dọn dẹp những session hết hạn hoặc không hoạt động
        self.cleanup_online_users()

        # Gắn số người online vào request để truy cập trong views
        request.online_count = self.get_online_count()

        return self.get_response(request)

    def increment_online_count(self):
        """ Tăng số người online """
        current_online = cache.get('online_count', 0)
        cache.set('online_count', current_online + 1, timeout=3600)

    def decrement_online_count(self):
        """ Giảm số người online """
        current_online = cache.get('online_count', 0)
        if current_online > 0:
            cache.set('online_count', current_online - 1, timeout=3600)

    def get_online_count(self):
        """ Lấy số người online hiện tại từ cache """
        return cache.get('online_count', 0)

    def cleanup_online_users(self):
        """ Dọn dẹp những người dùng không hoạt động quá 5 phút """
        active_sessions_key = 'active_sessions'
        active_sessions = cache.get(active_sessions_key, set())
        now = datetime.now()

        # Kiểm tra và loại bỏ những session không hoạt động (đã hết timeout 5 phút)
        for session_key in list(active_sessions):
            last_active = cache.get(session_key)
            if last_active and now - last_active > timedelta(seconds=300):  # 5 phút không hoạt động
                # Xóa session khỏi cache và giảm số người online
                cache.delete(session_key)
                active_sessions.remove(session_key)
                self.decrement_online_count()

        # Cập nhật lại danh sách session active
        cache.set(active_sessions_key, active_sessions, timeout=3600)

