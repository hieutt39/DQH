from django.http import JsonResponse
from src.modules.tools.models import SiteStatistics

def get_stats(request):
    # Lấy số người đang online từ middleware
    online_count = getattr(request, 'online_count', 0)

    # Lấy tổng lượng truy cập từ database
    total_visits = SiteStatistics.objects.first().total_visits if SiteStatistics.objects.exists() else 0

    # Trả về kết quả
    return JsonResponse({
        'online_count': online_count,
        'total_visits': total_visits,
    })
