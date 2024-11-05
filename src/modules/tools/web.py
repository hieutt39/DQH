import datetime

from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _
from src.utilities.extract_db.core import *


# @login_required(login_url="admin:login")
def index(request, template_name='web/index.html'):
    return TemplateResponse(request, template_name, {})

def khamphathegioimatuy(request, template_name='web/khamphathegioimatuy.html'):
    return TemplateResponse(request, template_name, {})

def test(request, template_name='web/layout.html'):
    return TemplateResponse(request, template_name, {})
