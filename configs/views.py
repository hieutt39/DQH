from django.http import JsonResponse
from src.utilities.analytics import get_analytics_data

def analytics_view(request):
    analytics_data = get_analytics_data()  # Lấy dữ liệu từ API
    if analytics_data is None:
        analytics_data = {"active_users": 0, "total_visits": 0}  # Phòng trường hợp API lỗi
    
    # Trả về dữ liệu dưới dạng JSON
    return JsonResponse(analytics_data)
