import datetime

from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _
from src.utilities.extract_db.core import *


# @login_required(login_url="admin:login")
def index(request, template_name='web/index.html'):
    return TemplateResponse(request, template_name, {})


def quiz_index(request, template_name='web/quiz_index.html'):
    return TemplateResponse(request, template_name, {})


def kptgmt_pdf(request, id, template_name='web/kptgmt_pdf.html'):
    file_name = '00 Ma túy là gì.pdf'
    if int(id) == 2:
        file_name = '01 Ma túy có mấy loại.pdf'
    elif int(id) == 3:
        file_name = '1. Ma túy tự nhiên.pdf'
    elif int(id) == 4:
        file_name = '1.1. Thuốc phiện.pdf'
    elif int(id) == 5:
        file_name = '1.2. Cocain.pdf'
    elif int(id) == 6:
        file_name = '1.3. Cần sa.pdf'
    elif int(id) == 7:
        file_name = '1.4. Nấm thức thần (nấm ma thuật).pdf'
    elif int(id) == 8:
        file_name = '1.5. Lá Khat.pdf'
    elif int(id) == 9:
        file_name = '2. Ma túy bán tổng hợp.pdf'
    elif int(id) == 10:
        file_name = '2.1. Heroin.pdf'
    elif int(id) == 11:
        file_name = '2.2. Morphine.pdf'
    elif int(id) == 12:
        file_name = '3. Ma túy tổng hợp.pdf'
    elif int(id) == 13:
        file_name = '3.1. Thuốc lắc (ectasy).pdf'
    elif int(id) == 14:
        file_name = '3.2. Ma túy đá (meth).pdf'
    elif int(id) == 15:
        file_name = '3.3. Lysergic acid diethylamide (viên giấy, bùa lưỡi).pdf'
    elif int(id) == 16:
        file_name = '3.4. Cỏ Mỹ.pdf'
    elif int(id) == 17:
        file_name = '3.5. Amphetamine.pdf'
    elif int(id) == 18:
        file_name = '4. Một số loại ma túy phổ biến.pdf'
    elif int(id) == 19:
        file_name = '000 Chất Ma Túy Ngụy Trang.pdf'
    elif int(id) == 20:
        file_name = '001 Các chất ma túy thế hệ mới.pdf'

    return TemplateResponse(request, template_name, {
        'file_name': file_name
    })


def ndccmt_video(request, template_name='web/kptgmt_pdf.html'):
    return TemplateResponse(request, template_name, {})


def thcmt_video(request, template_name='web/kptgmt_pdf.html'):
    return TemplateResponse(request, template_name, {})


def thcmt_pdf(request, id, template_name='web/thcmt_pdf.html'):
    file_name = '5.1. Nghiện ma túy là gì.pdf'
    if int(id) == 2:
        file_name = '5.2. Các dấu hiệu để nhận biết người bị nghiện ma túy.pdf'
    elif int(id) == 3:
        file_name = '5.3. Bạn có thể chết nếu sử dụng ma túy không.pdf'
    elif int(id) == 4:
        file_name = '5.4. Tác hại của ma túy.pdf'
    elif int(id) == 5:
        file_name = '5.5. Các phương pháp điều trị cai nghiện.pdf'
    elif int(id) == 6:
        file_name = '6.1. HIV-AIDS là gì.pdf'
    elif int(id) == 7:
        file_name = '6.2. Mối liên hệ giữa ma túy và HIV-AIDS.pdf'
    elif int(id) == 8:
        file_name = '6.3. HIV lây truyền như thế nào.pdf'
    elif int(id) == 9:
        file_name = '6.4. Cần làm gì để phòng tránh lây, nhiễm HIV.pdf'
    return TemplateResponse(request, template_name, {
        'file_name': file_name
    })


def knpcmt_pdf(request, id, template_name='web/knpcmt_pdf.html'):
    file_name = '7.1. Kỹ năng ứng phó với ma túy.pdf'
    if int(id) == 2:
        file_name = '7.2. Kỹ năng quản lý cảm xúc.pdf'
    elif int(id) == 3:
        file_name = '7.3. Kỹ năng ứng phó với căng thẳng.pdf'
    elif int(id) == 4:
        file_name = '7.4. Kỹ năng tìm kiếm trợ giúp.pdf'
    elif int(id) == 5:
        file_name = '7.5. Một số tình huống trong thực tiễn.pdf'
    elif int(id) == 6:
        file_name = '7.6. Hotline tư vấn.pdf'
    elif int(id) == 7:
        file_name = 'Vai Trò Của Giáo Viên Trong Phòng Tránh ma túy học đường.pdf'
    elif int(id) == 8:
        file_name = 'Vai Trò Của Phụ Huynh Trong Phòng Tránh ma túy học đường.pdf'

    return TemplateResponse(request, template_name, {
        'file_name': file_name
    })
