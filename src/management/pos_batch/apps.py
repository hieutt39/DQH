from django.apps import AppConfig


class MigrateThgConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.modules.the'

# src/modules/the/apps.py

from django.apps import AppConfig
from django.contrib.sessions import session_deleted

# Đảm bảo bạn đã định nghĩa hàm xử lý tín hiệu
def session_expired(sender, instance, **kwargs):
    print(f"Session {instance.session_key} đã bị xóa!")

class MigrateThgConfig(AppConfig):
    name = 'src.modules.the'

    def ready(self):
        # Đăng ký tín hiệu trực tiếp trong phương thức ready
        session_deleted.connect(session_expired)

