# views.py
from django.shortcuts import render
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.http import JsonResponse
def get_stats(request):
    # Đếm số người online: Tính dựa trên session còn hạn
    online_count = Session.objects.filter(expire_date__gte=timezone.now()).count()

    # Đếm tổng lượng truy cập
    total_visits = cache.get('total_visits', 0)

    return JsonResponse({
        'online_count': online_count,
        'total_visits': total_visits
    })