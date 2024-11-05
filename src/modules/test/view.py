import datetime
import json

from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _

def index(request, template_name='test/index.html'):
    return TemplateResponse(request, template_name, {})
