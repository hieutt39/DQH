import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Đường dẫn tới file JSON chứa thông tin xác thực 
SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')

# Kiểm tra SERVICE_ACCOUNT_FILE
if not SERVICE_ACCOUNT_FILE or not os.path.exists(SERVICE_ACCOUNT_FILE):
    raise FileNotFoundError("SERVICE_ACCOUNT_FILE không được thiết lập hoặc file không tồn tại.")

# Phạm vi quyền cho Google Analytics API
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']

# GA4 Property ID 
PROPERTY_ID = '468896366'

def get_analytics_data():
    try:
        # Tạo thông tin xác thực
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        # Kết nối với Google Analytics Data API
        analytics = build('analyticsdata', 'v1beta', credentials=credentials)

        # Lấy dữ liệu real-time: số người dùng đang hoạt động
        realtime_response = analytics.properties().runRealtimeReport(
            property=f"properties/{PROPERTY_ID}",
            body={
                "dimensions": [{"name": "country"}],  # Lấy thông tin theo quốc gia
                "metrics": [{"name": "activeUsers"}],  # Số người dùng đang hoạt động
            }
        ).execute()

        # Lấy tổng lượng truy cập: tổng số sessions
        total_visits_response = analytics.properties().runReport(
            property=f"properties/{PROPERTY_ID}",
            body={
                "dateRanges": [{"startDate": "2024-09-09", "endDate": "today"}],
                "metrics": [{"name": "sessions"}],  # Tổng số sessions
            }
        ).execute()

        # Xử lý dữ liệu trả về
        active_users = (
            realtime_response['rows'][0]['metricValues'][0]['value']
            if 'rows' in realtime_response and realtime_response['rows']
            else 0
        )

        total_visits = (
            total_visits_response['rows'][0]['metricValues'][0]['value']
            if 'rows' in total_visits_response and total_visits_response['rows']
            else 0
        )

        # Trả về dữ liệu
        return {
            "active_users": active_users,
            "total_visits": total_visits,
        }

    except FileNotFoundError:
        print("Service Account file not found. Check SERVICE_ACCOUNT_FILE.")
        return None
    except HttpError as e:
        print(f"An error occurred with the Google Analytics API: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

# Gọi hàm và in kết quả
analytics_data = get_analytics_data()

if analytics_data:
    print(f"Số người online: {analytics_data['active_users']}")
    print(f"Tổng lượng truy cập: {analytics_data['total_visits']}")
else:
    print("Không thể lấy dữ liệu từ Google Analytics.")
