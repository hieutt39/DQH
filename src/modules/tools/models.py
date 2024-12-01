import json
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext, gettext_lazy as _
from django.urls import reverse
import uuid


class SiteStatistics(models.Model):
    total_visits = models.PositiveIntegerField(default=0)

    @classmethod
    def increment_visits(cls):
        stats, created = cls.objects.get_or_create(id=1)  # Chỉ tạo một bản ghi duy nhất
        stats.total_visits += 1
        stats.save()
        return stats.total_visits
